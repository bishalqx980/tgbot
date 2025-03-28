import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from bot import logger
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
    
    # requied data needed for editing & callback query
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "bot_data",
        "search_key": "_id",
        "match_value": MemoryDB.bot_data.get("_id"),
        "update_data_key": None,
        "update_data_value": None,
        "edit_value_message_id": None,
        "effective_message_id": effective_message.id
    }

    text = (
        "<u><b>Bot Settings</b></u>\n"
        "• Bot photo: <code>{}</code>\n"
        "• Images: <code>{}</code>\n"
        "• Support chat: <code>{}</code>\n"
        "• Server url: <code>{}</code>\n"
        "• Sudo: <code>{}</code>\n"
        "• Shrinkme API: <code>{}</code>\n"
        "• OMDB API: <code>{}</code>\n"
        "• Weather API: <code>{}</code>\n"
    )

    btn_data = [
        {"Bot Photo": "bsettings_bot_pic", "Images": "bsettings_images"},
        {"Support Chat": "bsettings_support_chat", "Server URL": "bsettings_server_url"},
        {"Sudo": "bsettings_sudo", "Shrinkme API": "bsettings_shrinkme_api"},
        {"OMDB API": "bsettings_omdb_api", "Weather API": "bsettings_weather_api"},
        {"> ⁅ Restore DB ⁆": "bsettings_restoredb", "Close": "bsettings_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    
    images = MemoryDB.bot_data.get("images")
    photo = random.choice(images).strip() if images else MemoryDB.bot_data.get("bot_pic")
    
    # storing data for memory update (storing before formatting text)
    data.update({"text": text, "btn": btn})

    # accessing bot data
    bot_data = MemoryDB.bot_data

    # formatting the message
    text = text.format(
        bot_data.get("bot_pic"),
        len(bot_data.get("images") or []),
        bot_data.get("support_chat"),
        bot_data.get("server_url"),
        len(bot_data.get("sudo_users") or []),
        bot_data.get("shrinkme_api"),
        bot_data.get("omdb_api"),
        bot_data.get("weather_api")
    )

    if photo:
        try:
            await effective_message.reply_photo(photo, text, reply_markup=btn)
        except BadRequest:
            photo = None
        except Exception as e:
            logger.error(e)
    
    if not photo:
        await effective_message.reply_text(text, reply_markup=btn)
    
    data.update({"is_caption": bool(photo)})
    MemoryDB.insert("data_center", user.id, data)
