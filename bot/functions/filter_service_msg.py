from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.telegram_helper import Message

async def func_filter_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
