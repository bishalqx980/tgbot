from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.utils.database.common import database_search
from ..auxiliary.pm_error import pm_error

async def func_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    chat_data = database_search("chats_data", "chat_id", chat.id)
    if not chat_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return

    filters = chat_data.get("filters")

    if filters:
        text = "<blockquote>Chat filters</blockquote>\n\n"
        for keyword in filters:
            text += f"• <code>{keyword}</code>\n"
    
    else:
        text = "This chat doesn't have any filters!"

    await effective_message.reply_text(text)
