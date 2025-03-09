from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.functions.filter_all import func_filter_all
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search

async def func_del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    only delete group chat commands
    """
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == ChatType.PRIVATE:
        return
    
    database = database_search("groups", "chat_id", chat.id)
    if database[0] == False:
        await Message.reply_message(update, database[1])
        return
    
    find_group = database[1]

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.delete_message(chat.id, msg)
    
    bot_commands = MemoryDB.bot_data.get("bot_commands")
    if bot_commands and msg.text not in bot_commands:
        await func_filter_all(update, context)
