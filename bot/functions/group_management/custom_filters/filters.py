from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.modules.database.common import database_search
from bot.functions.group_management.auxiliary.pm_error import pm_error

async def func_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return

    filters = database_data.get("filters")

    if filters:
        text = "<b><u>Chat filters</u></b>\n\n"
        for keyword in filters:
            text += f"• <code>{keyword}</code>\n"
    
    else:
        text = "This chat doesn't have any filters!"

    await effective_message.reply_text(text)
