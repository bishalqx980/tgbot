import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ChatMemberHandler
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
from bot.modules.group_management.invite_link import func_invite_link
from bot.modules.group_management.promote import func_promote
from bot.modules.group_management.demote import func_demote
from bot.modules.group_management.pin_msg import func_pin_msg
from bot.modules.group_management.unpin_msg import func_unpin_msg
from bot.modules.group_management.ban import func_ban
from bot.modules.group_management.unban import func_unban
from bot.modules.group_management.kick import func_kick
from bot.modules.group_management.kickme import func_kickme
from bot.modules.group_management.mute import func_mute
from bot.modules.group_management.unmute import func_unmute
from bot.modules.group_management.del_msg import func_del
from bot.modules.group_management.purge import func_purge
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
        await Message.send_msg(owner_id, "Warning! Server URL not provided!\nGoto /bsetting and setup server url then restart bot...")


def main():
    application = ApplicationBuilder().token(bot_token).build()
    # functions
    application.add_handler(CommandHandler("start", func_start, block=False))
    application.add_handler(CommandHandler("movie", func_movieinfo, block=False))
    application.add_handler(CommandHandler("tr", func_translator, block=False))
    application.add_handler(CommandHandler("decode", func_b64decode, block=False))
    application.add_handler(CommandHandler("encode", func_b64encode, block=False))
    application.add_handler(CommandHandler("short", func_shortener, block=False))
    application.add_handler(CommandHandler("ping", func_ping, block=False))
    application.add_handler(CommandHandler("calc", func_calc, block=False))
    application.add_handler(CommandHandler("webshot", func_webshot, block=False))
    application.add_handler(CommandHandler("weather", func_weather, block=False))
    application.add_handler(CommandHandler("imagine", func_imagine, block=False))
    application.add_handler(CommandHandler("gpt", func_chatgpt, block=False))
    application.add_handler(CommandHandler("ytdl", func_add_download_ytdl, block=False))
    application.add_handler(CommandHandler("yts", func_yts, block=False))
    application.add_handler(CommandHandler("qr", func_gen_qr, block=False))
    application.add_handler(CommandHandler("itl", func_img_to_link, block=False))
    application.add_handler(CommandHandler("settings", func_settings, block=False))
    application.add_handler(CommandHandler("id", func_id, block=False))
    application.add_handler(CommandHandler("invite", func_invite_link, block=False))
    application.add_handler(CommandHandler("promote", func_promote, block=False))
    application.add_handler(CommandHandler("demote", func_demote, block=False))
    application.add_handler(CommandHandler("pin", func_pin_msg, block=False))
    application.add_handler(CommandHandler("unpin", func_unpin_msg, block=False))
    application.add_handler(CommandHandler("ban", func_ban, block=False))
    application.add_handler(CommandHandler("unban", func_unban, block=False))
    application.add_handler(CommandHandler("kick", func_kick, block=False))
    application.add_handler(CommandHandler("kickme", func_kickme, block=False))
    application.add_handler(CommandHandler("mute", func_mute, block=False))
    application.add_handler(CommandHandler("unmute", func_unmute, block=False))
    application.add_handler(CommandHandler("del", func_del, block=False))
    application.add_handler(CommandHandler("purge", func_purge, block=False))
    application.add_handler(CommandHandler("lock", func_lockchat, block=False))
    application.add_handler(CommandHandler("unlock", func_unlockchat, block=False))
    application.add_handler(CommandHandler("filter", func_filter, block=False))
    application.add_handler(CommandHandler("remove", func_remove, block=False))
    application.add_handler(CommandHandler("filters", func_filters, block=False))
    application.add_handler(CommandHandler("adminlist", func_adminlist, block=False))
    application.add_handler(CommandHandler("help", func_help, block=False))
    # owner
    application.add_handler(CommandHandler("broadcast", func_broadcast, block=False))
    application.add_handler(CommandHandler("db", func_database, block=False))
    application.add_handler(CommandHandler("bsetting", func_bsettings, block=False))
    application.add_handler(CommandHandler("shell", func_shell, block=False))
    application.add_handler(CommandHandler("log", func_log, block=False))
    application.add_handler(CommandHandler("restart", func_restart, block=False))
    application.add_handler(CommandHandler("sys", func_sys, block=False))
    # filters
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, func_filter_services, block=False))
    application.add_handler(MessageHandler(filters.ALL, func_filter_all, block=False))
    # Chat Member Handler
    application.add_handler(ChatMemberHandler(track_bot_chat_act, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking bot/private chat
    application.add_handler(ChatMemberHandler(track_other_chat_act, ChatMemberHandler.CHAT_MEMBER)) # for tacking group/supergroup
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
