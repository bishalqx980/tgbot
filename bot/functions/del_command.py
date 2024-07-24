import json
from telegram import Update
from telegram.ext import ContextTypes
from bot.functions.filter_all import func_filter_all
from bot.helper.telegram_helper import Message
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
        await Message.reply_msg(update, db[1])
        return
    
    find_group = db[1]

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.del_msg(chat.id, msg)
    
    bot_cmds = json.load(open("bot_cmds.json", "r"))
    bot_commands = bot_cmds.get("bot_commands")
    
    if msg.text not in bot_commands:
        await func_filter_all(update, context)
