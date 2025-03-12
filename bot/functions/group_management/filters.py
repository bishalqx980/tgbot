from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.modules.database.common import database_search

from bot.functions.group_management.pm_error import _pm_error

async def func_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return
    
    
    
    response, database_data = database_search("groups", "chat_id", chat.id)
    if database[0] == False:
        await effective_message.reply_text(database[1])
        return
    
    find_group = database[1]

    filters = find_group.get("filters")

    msg = f"<b><u>Chat filters</u></b>\n\n"
    if filters:
        for keyword in filters:
            msg += f"- <code>{keyword}</code>\n"
    else:
        msg += "- No filters\n"

    await effective_message.reply_text(msg)
