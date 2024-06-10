from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


async def _check_del_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    only delete group chat commands
    """
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == "private":
        return
    
    find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
    if not find_group:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
            return

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.del_msg(chat.id, msg)
