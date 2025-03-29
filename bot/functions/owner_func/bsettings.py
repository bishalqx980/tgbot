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
    
    # requied data needed for editing
    data = {
        "user_id": user.id, # authorization
        "collection_name": "bot_data",
        "search_key": "_id",
        "match_value": MemoryDB.bot_data.get("_id")
    }

    MemoryDB.insert("data_center", user.id, data)

    # accessing bot data
    bot_data = MemoryDB.bot_data

    text = (
        "<blockquote><b>Bot Settings</b></blockquote>\n"
        f"• Bot photo: <code>{bot_data.get('bot_pic')}</code>\n"
        f"• Images: <code>{len(bot_data.get('images') or [])}</code>\n"
        f"• Support chat: <code>{bot_data.get('support_chat')}</code>\n"
        f"• Server url: <code>{bot_data.get('server_url')}</code>\n"
        f"• Sudo: <code>{len(bot_data.get('sudo_users') or [])}</code>\n"
        f"• Shrinkme API: <code>{bot_data.get('shrinkme_api')}</code>\n"
        f"• OMDB API: <code>{bot_data.get('omdb_api')}</code>\n"
        f"• Weather API: <code>{bot_data.get('weather_api')}</code>"
    )
    
    btn_data = [
        {"Bot Photo": "bsettings_bot_pic", "Images": "bsettings_images"},
        {"Support Chat": "bsettings_support_chat", "Server URL": "bsettings_server_url"},
        {"Sudo": "bsettings_sudo", "Shrinkme API": "bsettings_shrinkme_api"},
        {"OMDB API": "bsettings_omdb_api", "Weather API": "bsettings_weather_api"},
        {"> ⁅ Restore DB ⁆": "bsettings_restoredb", "Close": "bsettings_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    
    images = bot_data.get("images")
    photo = random.choice(images).strip() if images else bot_data.get("bot_pic")

    if photo:
        try:
            await effective_message.reply_photo(photo, text, reply_markup=btn)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo
    await effective_message.reply_text(text, reply_markup=btn)
