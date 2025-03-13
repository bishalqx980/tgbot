import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.functions.sudo_users import fetch_sudos

async def func_bsettings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "bot_data",
        "db_find": "_id",
        "db_vlaue": MemoryDB.bot_data.get("_id"),
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": effective_message.id,
        "edit_data_value_msg_pointer_id": None
    }

    MemoryDB.insert_data("data_center", user.id, data)
    
    text = "<u><b>Bot Settings</b></u>"

    btn_data = [
        {"Bot pic": "query_bot_pic", "Images": "query_images"},
        {"Support chat": "query_support_chat", "Server url": "query_server_url"},
        {"Sudo": "query_sudo", "Shrinkme API": "query_shrinkme_api"},
        {"OMDB API": "query_omdb_api", "Weather API": "query_weather_api"},
        {"> Restore DB?": "query_restore_db", "Close": "query_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    
    images = MemoryDB.bot_data.get("images")
    photo = random.choice(images).strip() if images else MemoryDB.bot_data.get("bot_pic")
    if photo:
        await effective_message.reply_photo(photo, text, reply_markup=btn)
    else:
        await effective_message.reply_text(text, reply_markup=btn)
