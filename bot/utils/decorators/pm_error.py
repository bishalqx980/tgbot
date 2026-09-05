from functools import wraps

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ChatType


def pm_error(func):
    @wraps(func)
    async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """:param chat_id: where you want to send this *pm_error* message"""
        chat = update.effective_chat

        if chat.type in [ChatType.PRIVATE]:
            return await context.bot.send_message(
                chat.id,
                "This command is made to be used in group chats, not in pm!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Add me to your chat", f"http://t.me/{context.bot.username}?startgroup=help")
                ]])
            )
        
        return await func(update, context)
    return wraper
