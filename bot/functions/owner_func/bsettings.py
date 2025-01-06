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
        await Message.reply_message(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    _bot = await find_bot_docs()
    if not _bot:
        return
    
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

    btn_data_row1 = {
        "Bot pic": "query_bot_pic",
        "Welcome img": "query_welcome_img"
    }

    btn_data_row2 = {
        "Images": "query_images",
        "Support chat": "query_support_chat"
    }

    btn_data_row3 = {
        "Server url": "query_server_url",
        "Sudo": "query_sudo"
    }

    btn_data_row4 = {
        "Shrinkme API": "query_shrinkme_api",
        "OMDB API": "query_omdb_api"
    }

    btn_data_row5 = {
        "Weather API": "query_weather_api",
        "ImgBB API": "query_imgbb_api"
    }

    btn_data_row6 = {
        "> Restore DB?": "query_restore_db",
        "Close": "query_close"
    }

    row1 = await Button.cbutton(btn_data_row1, True)
    row2 = await Button.cbutton(btn_data_row2, True)
    row3 = await Button.cbutton(btn_data_row3, True)
    row4 = await Button.cbutton(btn_data_row4, True)
    row5 = await Button.cbutton(btn_data_row5, True)
    row6 = await Button.cbutton(btn_data_row6, True)

    btn = row1 + row2 + row3 + row4 + row5 + row6

    _bot = await find_bot_docs()
    if not _bot:
        return
    
    images = _bot.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = _bot.get("bot_pic")
    
    sent_img = await Message.send_image(chat.id, image, msg, btn=btn) if image else None
    if not sent_img:
        await Message.send_message(chat.id, msg, btn=btn)
