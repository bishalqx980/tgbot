import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ..sudo_users import fetch_sudos

async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([effective_message.id, sent_message.id])
        return
    
    await effective_message.reply_document(open("sys/log.txt", "rb"), filename="log.txt")
