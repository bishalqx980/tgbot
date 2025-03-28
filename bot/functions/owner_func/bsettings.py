import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.messages_storage import bot_settings_menu
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
        "edit_value_message_id": None,
        "effective_message_id": effective_message.id
    }

    MemoryDB.insert_data("data_center", user.id, data)
    
    bot_data = MemoryDB.bot_data
    bot_pic = bot_data.get("bot_pic")
    images = len(bot_data.get("images") or [])
    support_chat = bot_data.get("support_chat")
    server_url = bot_data.get("server_url")
    sudo_users = len(bot_data.get("sudo_users") or [])
    shrinkme_api = bot_data.get("shrinkme_api")
    omdb_api = bot_data.get("omdb_api")
    weather_api = bot_data.get("weather_api")

    text = bot_settings_menu.format(
        bot_pic,
        images,
        support_chat,
        server_url,
        sudo_users,
        shrinkme_api,
        omdb_api,
        weather_api
    )

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
        try:
            await effective_message.reply_photo(photo, text, reply_markup=btn)
        except BadRequest:
            photo = None
        except Exception as e:
            logger.error(e)
    
    if not photo:
        await effective_message.reply_text(text, reply_markup=btn)
