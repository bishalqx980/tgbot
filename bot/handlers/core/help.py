import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from telegram.helpers import create_deep_linked_url
from bot import logger
from bot.helpers import BuildKeyboard
from bot.utils.database import MemoryDB
from bot.utils.database.common import database_add_user

class HelpMenuData:
    TEXT = (
        "<blockquote><b>Help Menu</b></blockquote>\n\n"
        "Hey! Welcome to the bot help section.\n"
        "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
        "• /start - Start the bot\n"
        "• /help - To see this message\n"
        "• /support - Get Support or Report any bug related to bot"
    )

    BUTTONS = [
        {"Group Management": "help_menu_gm1", "AI/Info": "help_menu_ai_knowledge"},
        {"Misc": "help_menu_misc", "Owner/Sudo": "help_menu_owner"},
        {"» bot.info()": "help_menu_botinfo", "Close": "misc_close"}
    ]


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        btn = BuildKeyboard.ubutton([{"Click here for help": create_deep_linked_url(context.bot.username, "help")}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nContact me in PM for help!", reply_markup=btn)
        return
    
    # database entry checking if user is registered.
    database_add_user(user)

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
    
    btn = BuildKeyboard.cbutton(HelpMenuData.BUTTONS)
    
    if photo or photo_file_id:
        try:
            await effective_message.reply_photo(photo or photo_file_id, HelpMenuData.TEXT, reply_markup=btn)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo or Other error
    await effective_message.reply_text(HelpMenuData.TEXT, reply_markup=btn)
