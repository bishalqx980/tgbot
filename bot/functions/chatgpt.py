from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message

async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Message.reply_message(update, "This function has been disabled due to limitations! This maybe reintroduced in future updates.")
    return
