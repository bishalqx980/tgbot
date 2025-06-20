import asyncio
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType

def pm_only(func):
    @wraps(func)
    async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """:param chat_id: where you want to send this *pm_error* message"""
        chat = update.effective_chat

        if chat.type not in [ChatType.PRIVATE]:
            sent_message = await update.message.reply_text(f"This command is made to be used in pm, not in public chat!")
            await asyncio.sleep(3)
            await chat.delete_messages([update.message.id, sent_message.id])
            return
        
        return await func(update, context)
    return wraper
