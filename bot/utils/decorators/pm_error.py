from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.helpers import create_deep_linked_url
from bot.helpers import BuildKeyboard

def pm_error(func):
    @wraps(func)
    async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """:param chat_id: where you want to send this *pm_error* message"""
        chat = update.effective_chat

        if chat.type in [ChatType.PRIVATE]:
            btn = BuildKeyboard.ubutton([{"Add me to your chat": create_deep_linked_url(context.bot.username, "help", True)}])
            await context.bot.send_message(chat.id, "This command is made to be used in group chats, not in pm!", reply_markup=btn)
            return
        
        return await func(update, context)
    return wraper
