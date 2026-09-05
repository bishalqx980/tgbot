import random

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from bot import logger
from bot.utils.database import DBConstants, MemoryDB
from bot.utils.decorators.sudo_users import require_sudo
from bot.utils.decorators.pm_only import pm_only


class BotSettingsData:
    TEXT = (
        "<blockquote><b>Bot Settings</b></blockquote>\n\n"
        "• Show Bot Photo: <code>{}</code>\n"
        "• Images: <code>{}</code>\n"
        "• Support chat: <code>{}</code>\n"
        "• Server url: <code>{}</code>\n"
        "• Sudo: <code>{}</code>\n"
        "• Shrinkme API: <code>{}</code>\n"
        "• OMDB API: <code>{}</code>\n"
        "• Weather API: <code>{}</code>"
    )

    BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Show Bot Photo", callback_data="bsettings_show_bot_pic"),
            InlineKeyboardButton("Images", callback_data="bsettings_images")
        ],
        [
            InlineKeyboardButton("Support Chat", callback_data="bsettings_support_chat"),
            InlineKeyboardButton("Server URL", callback_data="bsettings_server_url")
        ],
        [
            InlineKeyboardButton("Sudo", callback_data="bsettings_sudo"),
            InlineKeyboardButton("Shrinkme API", callback_data="bsettings_shrinkme_api")
        ],
        [
            InlineKeyboardButton("OMDB API", callback_data="bsettings_omdb_api"),
            InlineKeyboardButton("Weather API", callback_data="bsettings_weather_api")
        ],
        [
            InlineKeyboardButton("> ⁅ Database ⁆", callback_data="bsettings_database"),
            InlineKeyboardButton("Close", callback_data="misc_close")
        ]
    ])


@pm_only
@require_sudo
async def func_bsettings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    
    # requied data needed for editing
    data = {
        "user_id": user.id, # authorization
        "collection_name": DBConstants.BOT_DATA,
        "search_key": "_id",
        "match_value": MemoryDB.bot_data.get("_id")
    }

    MemoryDB.insert(DBConstants.DATA_CENTER, user.id, data)

    # accessing bot data
    bot_data = MemoryDB.bot_data

    text = BotSettingsData.TEXT.format(
        'Yes' if bot_data.get('show_bot_pic') else 'No',
        len(bot_data.get('images') or []),
        bot_data.get('support_chat') or '-',
        bot_data.get('server_url') or '-',
        len(bot_data.get('sudo_users') or []),
        bot_data.get('shrinkme_api') or '-',
        bot_data.get('omdb_api') or '-',
        bot_data.get('weather_api') or '-'
    )
    
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
            await message.reply_photo(photo or photo_file_id, text, reply_markup=BotSettingsData.BUTTONS)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo or Other error
    await message.reply_text(text, reply_markup=BotSettingsData.BUTTONS)
