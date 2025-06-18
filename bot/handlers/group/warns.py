from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.decorators.pm_error import pm_error
from bot.utils.database import database_search
from .auxiliary.chat_admins import ChatAdmins

@pm_error
async def func_warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, user_id=user.id)

    if chat_admins.is_user_admin or chat_admins.is_user_owner:
        await effective_message.reply_text("How could someone give you a warning?")
        return
    
    chat_data = database_search("chats_data", "chat_id", chat.id)
    if not chat_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    warns = chat_data.get("warns") or {}
    victim_warns = warns.get(str(user.id)) or {} # mongodb doesn't allow int doc key

    warn_count = victim_warns.get("count")

    if not warn_count:
        text = "🎉 Congratulations, you don't have any warning in this chat!"
    else:
        text = f"You have {warn_count}/3 warnings!! Be careful...!"
    
    await effective_message.reply_text(text)
