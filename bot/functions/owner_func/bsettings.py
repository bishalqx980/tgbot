import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from bot import logger
from bot.helper.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from ..sudo_users import fetch_sudos

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
        "<blockquote><b>Bot Settings</b></blockquote>\n\n"
        f"• Show Bot Photo: <code>{bot_data.get('show_bot_pic') or False}</code>\n"
        f"• Images: <code>{len(bot_data.get('images') or [])}</code>\n"
        f"• Support chat: <code>{bot_data.get('support_chat')}</code>\n"
        f"• Server url: <code>{bot_data.get('server_url')}</code>\n"
        f"• Sudo: <code>{len(bot_data.get('sudo_users') or [])}</code>\n"
        f"• Shrinkme API: <code>{bot_data.get('shrinkme_api')}</code>\n"
        f"• OMDB API: <code>{bot_data.get('omdb_api')}</code>\n"
        f"• Weather API: <code>{bot_data.get('weather_api')}</code>"
    )
    
    btn_data = [
        {"Show Bot Photo": "bsettings_show_bot_pic", "Images": "bsettings_images"},
        {"Support Chat": "bsettings_support_chat", "Server URL": "bsettings_server_url"},
        {"Sudo": "bsettings_sudo", "Shrinkme API": "bsettings_shrinkme_api"},
        {"OMDB API": "bsettings_omdb_api", "Weather API": "bsettings_weather_api"},
        {"> ⁅ Database ⁆": "bsettings_database", "Close": "bsettings_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    
    show_bot_pic = MemoryDB.bot_data.get("show_bot_pic")
    images = MemoryDB.bot_data.get("images")
    photo = None
    photo_file_id = None

    if images:
        photo = random.choice(images).strip()
    elif show_bot_pic:
        try:
            bot_photos = await context.bot.get_user_profile_photos(context.bot.id)
            photo_file_id = bot_photos.photos[0][-1].file_id # the high quality photo file_id
        except:
            pass
    
    if photo or photo_file_id:
        try:
            await effective_message.reply_photo(photo or photo_file_id, text, reply_markup=btn)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo or Other error
    await effective_message.reply_text(text, reply_markup=btn)
