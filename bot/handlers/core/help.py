import random

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest

from bot import logger
from bot.utils.database import MemoryDB, database_add_user


class HelpMenuData:
    TEXT = (
        "<blockquote><b>Help Menu</b></blockquote>\n\n"
        "Hey! Welcome to the bot help section.\n"
        "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
        "• /start - Start the bot\n"
        "• /help - To see this message\n"
        "• /support - Get Support or Report any bug related to bot"
    )

    BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Group Management", callback_data="help_menu_gm1"),
            InlineKeyboardButton("AI", callback_data="help_menu_ai_knowledge")
        ],
        [
            InlineKeyboardButton("Misc", callback_data="help_menu_misc"),
            InlineKeyboardButton("Owner/Sudo", callback_data="help_menu_owner")
        ],
        [
            InlineKeyboardButton("» bot.info()", callback_data="help_menu_botinfo"),
            InlineKeyboardButton("Close", callback_data="misc_close"),
            InlineKeyboardButton("Try inline", switch_inline_query_current_chat="")
        ]
    ])


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type not in [ChatType.PRIVATE]:
        return await effective_message.reply_text(
            f"Hey, {user.first_name}\nContact me in PM for help!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Click here for help", f"http://t.me/{context.bot.username}?start=help")
            ]])
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
    
    try:
        if photo or photo_file_id:
            try:
                await effective_message.reply_photo(
                    photo or photo_file_id, HelpMenuData.TEXT,
                    reply_markup=HelpMenuData.BUTTONS
                )
                return
            except BadRequest:
                pass
            except Exception as e:
                logger.error(e)
        
        # if BadRequest or No Photo or Other error
        await effective_message.reply_text(
            HelpMenuData.TEXT,
            reply_markup=HelpMenuData.BUTTONS
        )
    except Exception as e:
        logger.error(e)
    
    finally:
        # database entry checking if user is registered.
        database_add_user(user)
