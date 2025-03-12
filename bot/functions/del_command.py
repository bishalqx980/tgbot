from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.functions.filters.text_caption import func_filter_text_caption
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search

async def func_del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Note: only delete group chat commands
    """
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type == ChatType.PRIVATE:
        return
    
    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return

    del_cmd = database_data.get("del_cmd")
    if del_cmd:
        await effective_message.delete()
    
    # bot_commands = MemoryDB.bot_data.get("bot_commands")
    # if bot_commands and effective_message.text not in bot_commands:
    #     await func_filter_text_caption(update, context)
