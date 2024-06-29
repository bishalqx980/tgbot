import asyncio
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ChatMemberHandler
)
from bot import bot_token, logger, owner_id
from bot.update_db import update_database
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.functions.power_users import _power_users
from bot.functions.start import func_start
from bot.functions.movieinfo import func_movieinfo
from bot.functions.translator import func_translator
from bot.functions.b64decode import func_b64decode
from bot.functions.b64encode import func_b64encode
from bot.functions.shortener import func_shortener
from bot.functions.ping import func_ping
from bot.functions.calc import func_calc
from bot.functions.webshot import func_webshot
from bot.functions.weather import func_weather
from bot.functions.imagine import func_imagine
from bot.functions.chatgpt import func_chatgpt
from bot.functions.youtube_dl import func_add_download_ytdl
from bot.functions.youtube_search import func_yts
from bot.functions.gen_qr import func_gen_qr
from bot.functions.img_to_link import func_img_to_link
from bot.functions.settings import func_settings
from bot.functions.id import func_id
from bot.functions.help import func_help
from bot.functions.broadcast import func_broadcast
from bot.functions.database import func_database
from bot.functions.bsettings import func_bsettings
from bot.functions.shell import func_shell
from bot.functions.log import func_log
from bot.functions.restart import func_restart
from bot.functions.sys import func_sys
from bot.functions.filter_service_msg import func_filter_services
from bot.functions.filter_all import func_filter_all
from bot.functions.del_command import func_del_command
from bot.modules.group_management.invite_link import func_invite_link
from bot.modules.group_management.promote import func_promote, func_spromote
from bot.modules.group_management.demote import func_demote, func_sdemote
from bot.modules.group_management.pin_msg import func_pin_msg, func_spin_msg
from bot.modules.group_management.unpin_msg import func_unpin_msg, func_sunpin_msg
from bot.modules.group_management.unpinall_msg import func_unpinall_msg, func_sunpinall_msg
from bot.modules.group_management.ban import func_ban, func_sban
from bot.modules.group_management.unban import func_unban, func_sunban
from bot.modules.group_management.kick import func_kick, func_skick
from bot.modules.group_management.kickme import func_kickme
from bot.modules.group_management.mute import func_mute, func_smute
from bot.modules.group_management.unmute import func_unmute, func_sunmute
from bot.modules.group_management.del_msg import func_del, func_sdel
from bot.modules.group_management.purge import func_purge, func_spurge
from bot.modules.group_management.lock_chat import func_lockchat
from bot.modules.group_management.unlock_chat import func_unlockchat
from bot.modules.group_management.add_filter import func_filter
from bot.modules.group_management.remove_filter import func_remove
from bot.modules.group_management.filters import func_filters
from bot.modules.group_management.adminlist import func_adminlist
from bot.modules.group_management.track_bot_chat import track_bot_chat_act
from bot.modules.group_management.track_other_chat import track_other_chat_act
from bot.helper.callbackbtn_helper import func_callbackbtn


async def server_alive():
    server_url = await MongoDB.get_data("bot_docs", "server_url")
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    power_users = await _power_users()
    
    try:
        if not bot_status or bot_status == "alive":
            for user_id in power_users:
                try:
                    await Message.send_msg(user_id, "Bot Started!")
                except Exception as e:
                    logger.error(e)
        elif bot_status == "restart":
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
            for user_id in power_users:
                try:
                    await Message.send_msg(user_id, "Bot Restarted!")
                except Exception as e:
                    logger.error(e)
    except Exception as e:
        logger.error(e)

    if server_url:
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        while True:
            try:
                response = requests.get(server_url)
                if response.status_code == 200:
                    logger.info(f"{server_url} is up and running. ✅")
                else:
                    logger.warning(f"{server_url} is down or unreachable. ❌")
            except Exception as e:
                logger.error(f"{server_url} > {e}")
            await asyncio.sleep(180) # 3 min
    else:
        logger.warning("Server URL not provided !!")
        await Message.send_msg(owner_id, "Warning! Server URL not provided!\nGoto /bsettings and setup server url then restart bot...")


def main():
    application = ApplicationBuilder().token(bot_token).build()
    # functions
    commands = {
        "start": func_start,
        "movie": func_movieinfo,
        "tr": func_translator,
        "decode": func_b64decode,
        "encode": func_b64encode,
        "short": func_shortener,
        "ping": func_ping,
        "calc": func_calc,
        "webshot": func_webshot,
        "weather": func_weather,
        "imagine": func_imagine,
        "gpt": func_chatgpt,
        "ytdl": func_add_download_ytdl,
        "yts": func_yts,
        "qr": func_gen_qr,
        "itl": func_img_to_link,
        "settings": func_settings,
        # Group management
        "id": func_id,
        "invite": func_invite_link,
        "promote": func_promote,
        "spromote": func_spromote,
        "demote": func_demote,
        "sdemote": func_sdemote,
        "pin": func_pin_msg,
        "spin": func_spin_msg,
        "unpin": func_unpin_msg,
        "sunpin": func_sunpin_msg,
        "unpinall": func_unpinall_msg,
        "sunpinall": func_sunpinall_msg,
        "ban": func_ban,
        "sban": func_sban,
        "unban": func_unban,
        "sunban": func_sunban,
        "kick": func_kick,
        "skick": func_skick,
        "kickme": func_kickme,
        "mute": func_mute,
        "smute": func_smute,
        "unmute": func_unmute,
        "sunmute": func_sunmute,
        "del": func_del,
        "sdel": func_sdel,
        "purge": func_purge,
        "spurge": func_spurge,
        "lock": func_lockchat,
        "unlock": func_unlockchat,
        "filter": func_filter,
        "remove": func_remove,
        "filters": func_filters,
        "adminlist": func_adminlist,
        "help": func_help,
        # owner commands...
        "broadcast": func_broadcast,
        "db": func_database,
        "bsettings": func_bsettings,
        "shell": func_shell,
        "log": func_log,
        "restart": func_restart,
        "sys": func_sys
    }

    for command, handler in commands.items():
        application.add_handler(CommandHandler(command, handler, block=False))
    
    # filters
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, func_filter_services, block=False))
    application.add_handler(MessageHandler(filters.COMMAND, func_del_command, block=False))
    application.add_handler(MessageHandler(filters.ALL, func_filter_all, block=False))
    # Chat Member Handler
    application.add_handler(ChatMemberHandler(track_bot_chat_act, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking bot/private chat
    application.add_handler(ChatMemberHandler(track_other_chat_act, ChatMemberHandler.CHAT_MEMBER)) # for tacking group/supergroup/channel
    # Callback button
    application.add_handler(CallbackQueryHandler(func_callbackbtn, block=False))
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    async def start_up_work():
        await update_database()
        await server_alive()
    
    loop = asyncio.get_event_loop()
    loop.create_task(start_up_work())
    loop.create_task(main())
    loop.run_forever()
