import os
import asyncio
import aiohttp
import importlib
from time import time
from telegram import Update, LinkPreviewOptions, BotCommand, BotCommandScope
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PrefixHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    Defaults
)
from telegram.error import BadRequest
from telegram.constants import ParseMode
from . import ENV_CONFIG, DEFAULT_ERROR_CHANNEL_ID, HANDLERS_DIR, BOT_HANDLERS_COUNT, bot, logger
from .alive import alive
from .update_db import update_database
from .modules import telegraph
from .modules.database import MemoryDB
from .functions.filters.text_caption import filter_text_caption
from .functions.query_handlers import (
    query_bot_settings,
    query_chat_settings,
    query_help_menu,
    query_misc,
    query_db_editing
)
from .functions.sudo_users import fetch_sudos
from .functions.bot_chats_tracker import bot_chats_tracker
from .functions.chat_status_update import chat_status_update


async def post_boot():
    # initializing telegraph
    await telegraph.initialize()

    # bot commands
    bot_commands = [
        BotCommand("start", "Introducing..."),
        BotCommand("help", "Bots help section...")
    ]
    
    try:
        # bot commands only for PRIVATE chats
        await bot.set_my_commands(bot_commands, BotCommandScope(BotCommandScope.ALL_PRIVATE_CHATS))
    except Exception as e:
        logger.error(e)

    # Send alive message to all sudo and bot owner
    sudo_users = fetch_sudos()

    try:
        await asyncio.gather(*(bot.send_message(user_id, "<b>Bot Started!</b>", parse_mode=ParseMode.HTML) for user_id in sudo_users))
    except Exception as e:
        logger.error(e)


async def server_alive():
    # executing after updating database so getting data from memory...
    server_url = MemoryDB.bot_data.get("server_url")
    if not server_url:
        logger.warning("✕ Server URL wasn't found.")

        text = (
            "✕ <code>Server URL</code> wasn't found!\n"
            "Bot may fall asleep. /bsettings to setup Server URL."
        )

        await bot.send_message(ENV_CONFIG["owner_id"], f"<b>{text}</b>", parse_mode=ParseMode.HTML)
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

    if update:
        user = update.effective_user
        chat = update.effective_chat
        effective_message = update.effective_message
        query = update.callback_query

        query_data = query.data if query else None
        chat_title = chat.full_name or chat.title if chat else None

        user_mention = user.mention_html() if user else None
        user_id = user.id if user else None
        chat_id = chat.id if chat else None
        effective_message_text = effective_message.text if effective_message else None

        text = (
            f"<b>⚠️ An error occured:</b>\n\n"
            f"<b>User:</b> {user_mention} | <code>{user_id}</code>\n"
            f"<b>Chat:</b> {chat_title} | <code>{chat_id}</code>\n"
            f"<b>Effective message:</b> <code>{effective_message_text}</code>\n"
            f"<b>Query message:</b> <code>{query_data}</code>\n\n"
            f"<pre>{context.error}</pre>"
        )
    else:
        text = (
            "<b>⚠️ An error occured:</b>\n\n"
            f"<pre>{context.error}</pre>"
        )

    try:
        await context.bot.send_message(DEFAULT_ERROR_CHANNEL_ID, text)
    except BadRequest:
        await context.bot.send_message(ENV_CONFIG["owner_id"], text)
    except Exception as e:
        logger.error(e)


def load_handlers():
    bot_commands = {}
    
    for root, dirs, files in os.walk(HANDLERS_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Constructing module path
                file_path = os.path.join(root, file)
                normalized_path = os.path.normpath(file_path)
                module_path = normalized_path.replace(os.sep, ".")

                if module_path.endswith(".py"):
                    module_path = module_path[:-3]
                
                # Importing the module
                module = importlib.import_module(module_path)
                
                # Iterate over all attributes in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    if callable(attr) and attr_name.startswith("func_"):
                        command_name = attr_name[len("func_"):]
                        bot_commands[command_name] = attr
    
    return bot_commands


def main():
    default_param = Defaults(
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        block=False,
        allow_sending_without_reply=True
    )
    # Bot instance
    application = ApplicationBuilder().token(ENV_CONFIG["bot_token"]).defaults(default_param).build()

    # Command handlers
    bot_commands = load_handlers()

    global BOT_HANDLERS_COUNT
    BOT_HANDLERS_COUNT.update({"bot_handlers_count": len(bot_commands)})

    logger.info(f"Modules loaded: {len(bot_commands)}")

    for command, handler in bot_commands.items():
        application.add_handler(CommandHandler(command, handler)) # for /command
        application.add_handler(PrefixHandler(["!", ".", "-"], command, handler)) # for other prefix command
    
    # filters
    application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, filter_text_caption))
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, chat_status_update)) # chat status update
    # Bot chat tracker
    application.add_handler(ChatMemberHandler(bot_chats_tracker, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking private chat
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(query_help_menu.query_help_menu, "help_menu_[A-Za-z0-9]+"))
    application.add_handler(CallbackQueryHandler(query_bot_settings.query_bot_settings, "bsettings_[A-Za-z0-9]+"))
    application.add_handler(CallbackQueryHandler(query_chat_settings.query_chat_settings, "csettings_[A-Za-z0-9]+"))
    application.add_handler(CallbackQueryHandler(query_misc.query_misc, "misc_[A-Za-z0-9]+"))
    application.add_handler(CallbackQueryHandler(query_db_editing.query_db_editing, "database_[A-Za-z0-9]+"))
    # Error handler
    application.add_error_handler(default_error_handler)
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


async def start_up_work():
    alive() # Server breathing
    update_database()
    await post_boot()
    await server_alive()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start_up_work())
    loop.create_task(main())
    loop.run_forever()
