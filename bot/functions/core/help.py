import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.messages_storage import (
    help_menu
)
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_add_user

async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        btn = ButtonMaker.ubutton([{"Click here for help": f"{context.bot.link}?start=help"}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nContact me in PM for help!", reply_markup=btn)
        return
    
    text = help_menu.format(user.full_name)

    btn_data = [
        {"Group Management": "query_help_group_management_p1", "AI": "query_help_ai"},
        {"misc": "query_help_misc_functions", "Bot owner": "query_help_owner_functions"},
        {"» bot.info()": "query_help_bot_info", "Close": "query_close"}
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
    
    database_add_user(user)
