import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from telegram.helpers import create_deep_linked_url
from ... import logger
from ...helper.button_maker import ButtonMaker
from ...modules.database import MemoryDB
from ...modules.database.common import database_add_user

async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        btn = ButtonMaker.ubutton([{"Click here for help": create_deep_linked_url(context.bot.username, "help")}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nContact me in PM for help!", reply_markup=btn)
        return
    
    # database entry checking if user is registered.
    database_add_user(user)
    
    text = (
        "<blockquote><b>Help Menu</b></blockquote>\n\n"
        "Hey! Welcome to the bot help section.\n"
        "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
        "• /start - Start the bot\n"
        "• /help - To see this message\n\n"
        "<blockquote><b>Note:</b> The bot is compatible with the <code>/</code>, <code>!</code>, <code>.</code> and <code>-</code> command prefixes.</blockquote>"
    )

    btn_data = [
        {"Group Management": "help_menu_gm1", "AI/Info": "help_menu_ai_knowledge"},
        {"Misc": "help_menu_misc", "Owner/Sudo": "help_menu_owner"},
        {"» bot.info()": "help_menu_botinfo", "Close": "help_menu_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)

    images = MemoryDB.bot_data.get("images")
    photo = random.choice(images).strip() if images else MemoryDB.bot_data.get("bot_pic")

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
