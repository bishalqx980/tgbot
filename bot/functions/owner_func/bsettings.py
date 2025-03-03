import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import find_bot_docs
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.power_users import _power_users


async def func_bsettings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_message(update, f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    _bot = await find_bot_docs()

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "bot_docs",
        "db_find": "_id",
        "db_vlaue": _bot.get("_id"),
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    await LOCAL_DATABASE.insert_data("data_center", user.id, data)
    
    msg = "<u><b>Bot Settings</b></u>"

    btn_data = [
        {"Bot pic": "query_bot_pic", "Welcome img": "query_welcome_img"},
        {"Images": "query_images", "Support chat": "query_support_chat"},
        {"Server url": "query_server_url", "Sudo": "query_sudo"},
        {"Shrinkme API": "query_shrinkme_api", "OMDB API": "query_omdb_api"},
        {"Weather API": "query_weather_api"},
        {"> Restore DB?": "query_restore_db", "Close": "query_close"}
    ]

    btn = await Button.cbutton(btn_data)
    
    images = _bot.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = _bot.get("bot_pic")
    
    sent_img = await Message.reply_image(update, image, msg, btn=btn) if image else None
    if not sent_img:
        await Message.reply_message(update, msg, btn=btn)
