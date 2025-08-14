import asyncio
import aiohttp
import traceback

from telegram import Update, LinkPreviewOptions, BotCommand, BotCommandScope
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    ConversationHandler,
    InlineQueryHandler,
    filters,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    Defaults
)
from telegram.error import BadRequest, Conflict, NetworkError, TimedOut
from telegram.constants import ChatID, ParseMode

from . import DEFAULT_ERROR_CHANNEL_ID, RUN_SERVER, bot, logger, config
from .utils.alive import alive
from .utils.update_db import update_database
from .modules import telegraph
from .utils.database import MemoryDB

from .handlers import (
    SUPPORT_STATES,
    init_support_conv,
    support_state_one,
    cancel_support_conv,

    func_start,
    func_help,

    filter_private_chat,
    filter_public_chat,

    func_adminlist,
    func_ban,
    join_request_handler,
    func_demote,
    func_invite,
    func_kick,
    func_kickme,
    func_lock,
    func_mute,
    func_pin,
    func_promote,
    func_purge,
    func_purgefrom,
    func_purgeto,
    func_unban,
    func_unlock,
    func_unmute,
    func_unpin,
    func_unpinall,
    func_warn,
    func_warns,
    func_whisper,

    func_filter,
    func_filters,
    func_remove,

    func_broadcast,
    func_bsettings,
    func_cadmins,
    func_database,
    func_invitelink,
    func_log,
    func_say,
    func_send,
    func_shell,
    func_sys,

    inline_query,
    query_admin_task,
    query_bot_settings,
    query_chat_settings,
    query_help_menu,
    query_misc,
    query_broadcast,
    query_db_editing,

    func_decode,
    func_encode,
    func_calc,
    func_gpt,
    func_decqr,
    func_genqr,
    func_rap,
    func_id,
    func_imagine,
    func_imgtolink,
    func_info,
    func_movie,
    func_paste,
    func_ping,
    func_psndl,
    func_settings,
    func_shorturl,
    func_tts,
    func_tr,
    func_unzip,
    func_weather,
    func_ytdl,
    
    bot_chats_tracker,
    chat_status_update
)


async def post_init():
    # initializing telegraph
    await telegraph.initialize()

    # bot pvt commands
    bot_pvt_commands = [
        BotCommand("start", "Introducing..."),
        BotCommand("help", "Bots help section..."),
        BotCommand("support", "Get Support or Report any bug related to bot...")
    ]

    # bot cadmin commands
    bot_cadmin_commands = [
        BotCommand("settings", "Chat settings...")
    ]
    
    try:
        # bot commands only for PRIVATE chats
        await bot.set_my_commands(bot_pvt_commands, BotCommandScope(BotCommandScope.ALL_PRIVATE_CHATS))
        # bot commands only for Chat admins
        await bot.set_my_commands(bot_cadmin_commands, BotCommandScope(BotCommandScope.ALL_CHAT_ADMINISTRATORS))
    except Exception as e:
        logger.error(e)

    # Send alive message to bot owner
    try:
        await bot.send_message(config.owner_id, "<blockquote><b>Bot Started!</b></blockquote>", parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(e)
    
    logger.info("Bot Started...")


async def server_alive():
    # executing after updating database so getting data from memory...
    if not RUN_SERVER:
        return
    
    server_url = MemoryDB.bot_data.get("server_url")
    if not server_url:
        logger.warning("'Server URL' wasn't found. Bot may fall asleep if deployed on Render (free instance)")
        return
    
    while True:
        # everytime check if there is new server_url
        server_url = MemoryDB.bot_data.get("server_url")
        if not server_url:
            return
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(server_url) as response:
                    if not response.ok:
                        logger.warning(f"{server_url} is down or unreachable. ❌ - code - {response.status}")
        except Exception as e:
            logger.error(f"{server_url} > {e}")
        await asyncio.sleep(180) # 3 min


async def default_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(context.error)
    auto_del_message = False

    if isinstance(context.error, (Conflict, NetworkError, TimedOut)):
        text = f"<blockquote>An error occured</blockquote>\n\n<code>{context.error}</code>"
        auto_del_message = True
    
    else:
        error_text = "".join(traceback.format_exception(type(context.error), context.error, context.error.__traceback__))
        # Remove excessive path details for readability
        error_text = "\n".join(line for line in error_text.split("\n") if "site-packages" not in line)
        # telegram message limit ?
        error_text = error_text[-2000:]

        text = (
            "<blockquote>An error occured</blockquote>\n\n"

            f"<b>• Type:</b> <code>{type(context.error).__name__}</code>\n"
            f"<b>• Message:</b> <code>{str(context.error)}</code>\n"
            "<b>• Traceback:</b>\n\n"
            f"<pre>{error_text}</pre>"
        )
    
    if DEFAULT_ERROR_CHANNEL_ID:
        try:
            sent_message = await context.bot.send_message(DEFAULT_ERROR_CHANNEL_ID, text)
            if auto_del_message:
                await asyncio.sleep(60)
                await sent_message.delete()
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
            return
    # if not DEFAULT_ERROR_CHANNEL_ID or BadRequest
    try:
        await context.bot.send_message(config.owner_id, text)
    except Exception as e:
        logger.error(e)


def main():
    default_param = Defaults(
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        block=False,
        allow_sending_without_reply=True
    )
    # Bot instance
    application = ApplicationBuilder().token(config.bot_token).defaults(default_param).build()

    # Conversation handlers
    application.add_handler(
        ConversationHandler(
            [CommandHandler("support", init_support_conv)],
            {
                SUPPORT_STATES.STATE_ONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_state_one)]
            },
            [CommandHandler("cancel", cancel_support_conv)]
        )
    )

    main_handlers = [
        CommandHandler("start", func_help, filters.Regex("help")), # this need to register before main start handler
        # core func
        CommandHandler("start", func_start),
        CommandHandler("help", func_help),
        # group management func
        CommandHandler("adminlist", func_adminlist),
        CommandHandler(["ban", "sban", "dban"], func_ban),
        CommandHandler(["demote", "sdemote"], func_demote),
        CommandHandler(["invite", "sinvite"], func_invite),
        CommandHandler(["kick", "skick", "dkick"], func_kick),
        CommandHandler("kickme", func_kickme),
        CommandHandler(["lock", "slock"], func_lock),
        CommandHandler(["mute", "smute", "dmute"], func_mute),
        CommandHandler(["pin", "spin"], func_pin),
        CommandHandler(["promote", "spromote"], func_promote),
        CommandHandler(["purge", "spurge"], func_purge),
        CommandHandler("purgefrom", func_purgefrom),
        CommandHandler("purgeto", func_purgeto),
        CommandHandler(["unban", "sunban"], func_unban),
        CommandHandler(["unlock", "sunlock"], func_unlock),
        CommandHandler(["unmute", "sunmute"], func_unmute),
        CommandHandler(["unpin", "sunpin"], func_unpin),
        CommandHandler(["unpinall", "sunpinall"], func_unpinall),
        CommandHandler(["warn", "dwarn"], func_warn),
        CommandHandler("warns", func_warns),
        CommandHandler("whisper", func_whisper),
        CommandHandler("filter", func_filter),
        CommandHandler("filters", func_filters),
        CommandHandler("remove", func_remove),
        # owner func
        CommandHandler("broadcast", func_broadcast),
        CommandHandler("bsettings", func_bsettings),
        CommandHandler("cadmins", func_cadmins),
        CommandHandler("database", func_database),
        CommandHandler("invitelink", func_invitelink),
        CommandHandler("log", func_log),
        CommandHandler("say", func_say),
        CommandHandler("send", func_send),
        CommandHandler("shell", func_shell),
        CommandHandler("sys", func_sys),
        # user func
        CommandHandler("decode", func_decode),
        CommandHandler("encode", func_encode),
        CommandHandler("calc", func_calc),
        CommandHandler("gpt", func_gpt),
        CommandHandler("decqr", func_decqr),
        CommandHandler("genqr", func_genqr),
        CommandHandler("rap", func_rap),
        CommandHandler("id", func_id),
        CommandHandler("imagine", func_imagine),
        CommandHandler("imgtolink", func_imgtolink),
        CommandHandler("info", func_info),
        CommandHandler("movie", func_movie),
        CommandHandler("paste", func_paste),
        CommandHandler("ping", func_ping),
        CommandHandler("psndl", func_psndl),
        CommandHandler("settings", func_settings), # part of group management also
        CommandHandler("shorturl", func_shorturl),
        CommandHandler("tts", func_tts),
        CommandHandler("tr", func_tr),
        CommandHandler("unzip", func_unzip),
        CommandHandler("weather", func_weather),
        CommandHandler("ytdl", func_ytdl)
    ]

    # main handlers register
    application.add_handlers(main_handlers)
    
    # Chat Join Request Handler
    application.add_handler(ChatJoinRequestHandler(join_request_handler))

    # filter private chat
    application.add_handler(MessageHandler(
        # SERVICE_CHAT is Linked channel with Group
        ~ filters.User(ChatID.SERVICE_CHAT) & filters.ChatType.PRIVATE & (filters.TEXT | filters.CAPTION),
        filter_private_chat.filter_private_chat
    ))
    # filter public chat
    application.add_handler(MessageHandler(
        # SERVICE_CHAT is Linked channel with Group
        ~ filters.User(ChatID.SERVICE_CHAT) & filters.ChatType.GROUPS & (filters.TEXT | filters.CAPTION),
        filter_public_chat.filter_public_chat
    ))
    # filter Chat Status Updates
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, chat_status_update))

    # Bot chat tracker (PRIVATE: only if bot is blocked or unblocked; PIUBLIC: any)
    application.add_handler(ChatMemberHandler(bot_chats_tracker, ChatMemberHandler.MY_CHAT_MEMBER))

    # Inline Query Handler
    application.add_handler(InlineQueryHandler(inline_query.inline_query_handler))

    # Callback query handlers
    application.add_handlers([
        CallbackQueryHandler(query_help_menu.query_help_menu, "help_menu_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_bot_settings.query_bot_settings, "bsettings_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_chat_settings.query_chat_settings, "csettings_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_admin_task.query_groupManagement, "admin_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_misc.query_misc, "misc_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_broadcast.query_broadcast, "broadcast_[A-Za-z0-9]+"),
        CallbackQueryHandler(query_db_editing.query_db_editing, "database_[A-Za-z0-9]+")
    ])

    # Error handler
    application.add_error_handler(default_error_handler)

    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


async def app_init():
    if RUN_SERVER:
        alive() # Server breathing
    # maintain the sequence
    update_database()
    await post_init()
    await server_alive()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(app_init())
    loop.create_task(main())
    loop.run_forever()
