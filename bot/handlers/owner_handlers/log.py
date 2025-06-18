import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([message.id, sent_message.id])
        return
    
    await message.reply_document(open("sys/log.txt", "rb"), filename="log.txt")
