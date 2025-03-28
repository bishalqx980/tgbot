from telegram import Update
from telegram.ext import ContextTypes

async def query_chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message



