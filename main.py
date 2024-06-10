import os
import sys
import time
import psutil
import random
import asyncio
import requests
import subprocess
from threading import Thread
from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ChatMemberHandler
from bot import logger, bot_token, bot, owner_id
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from bot.modules.ping_url import ping_url
from bot.modules.shrinkme import shortener_url
from bot.modules.translator import translate, LANG_CODE_LIST
from bot.modules.base64 import BASE64
from bot.modules.omdb_movie_info import get_movie_info
from bot.modules.utils import calc
from bot.modules.safone import Safone
from bot.modules.group_management.group_management import (
    _check_permission,
    track_my_chat_activities,
    track_chat_activities,
    _check_del_cmd,
    func_invite_link,
    func_promote,
    func_demote,
    func_pin_msg,
    func_unpin_msg,
    func_ban,
    func_unban,
    func_kick,
    func_kickme,
    func_mute,
    func_unmute,
    func_del,
    func_purge,
    func_lockchat,
    func_unlockchat,
    func_filter,
    func_remove,
    func_filters,
    func_adminlist)
from bot.modules.ytdl import YouTubeDownload
from bot.helper.callbackbtn_helper import func_callbackbtn
from bot.modules.weather import weather_info
from bot.modules.ai.g4f import G4F
from bot.update_db import update_database
from bot.modules.qr import QR
from bot.modules.telegraph import TELEGRAPH
from bot.modules.re_link_domain import RE_LINK
from bot.modules.database.local_database import LOCAL_DATABASE





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
    application.add_handler(CommandHandler("bsetting", func_bsetting, block=False))
    application.add_handler(CommandHandler("shell", func_shell, block=False))
    application.add_handler(CommandHandler("log", func_log, block=False))
    application.add_handler(CommandHandler("restart", func_restart, block=False))
    application.add_handler(CommandHandler("sys", func_sys, block=False))
    # filters
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, func_filter_services, block=False))
    application.add_handler(MessageHandler(filters.ALL, func_filter_all, block=False))
    # Chat Member Handler
    application.add_handler(ChatMemberHandler(track_my_chat_activities, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking bot/private chat
    application.add_handler(ChatMemberHandler(track_chat_activities, ChatMemberHandler.CHAT_MEMBER)) # for tacking group/supergroup
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
