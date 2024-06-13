from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.all_db_search import all_db_search


async def func_del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    only delete group chat commands
    """
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == "private":
        return
    
    db = await all_db_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_group = db[1]

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.del_msg(chat.id, msg)
