import os
import random
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
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
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
        "edit_data_value_msg_pointer": None
    }

    await LOCAL_DATABASE.insert_data("data_center", chat.id, data)
    
    btn_name_row1 = ["Bot pic", "Welcome img"]
    btn_data_row1 = ["query_bot_pic", "query_welcome_img"]

    btn_name_row2 = ["Images", "Support chat"]
    btn_data_row2 = ["query_images", "query_support_chat"]

    btn_name_row3 = ["Server url", "Sudo"]
    btn_data_row3 = ["query_server_url", "query_sudo"]

    btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
    btn_data_row4 = ["query_shrinkme_api", "query_omdb_api", "query_weather_api"]

    btn_name_row5 = ["> Restore DB?", "Close"]
    btn_data_row5 = ["query_restore_db", "query_close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
    row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
    row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

    btn = row1 + row2 + row3 + row4 + row5
    
    os.makedirs("back_btn", exist_ok=True)
    with open(f"back_btn/{chat.id}.txt", "wb") as f:
        f.write(btn)

    _bot = await find_bot_docs()
    if not _bot:
        return
    
    images = _bot.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = _bot.get("bot_pic")
    
    if image:
        await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
    else:
        await Message.send_msg(chat.id, "<u><b>Bot Settings</b></u>", btn)
