import json
from telegram import Update
from telegram.ext import ContextTypes
from bot.functions.filter_all import func_filter_all
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.modules.database.combined_db import global_search

async def func_del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    only delete group chat commands
    """
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == "private":
        return
    
    db = await global_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.reply_message(update, db[1])
        return
    
    find_group = db[1]

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.delete_message(chat.id, msg)
    
    load_bot_commands = json.load(open("sys/bot_commands.json", "r"))
    bot_commands = load_bot_commands.get("bot_commands")
    
    if msg.text not in bot_commands:
        await func_filter_all(update, context)
