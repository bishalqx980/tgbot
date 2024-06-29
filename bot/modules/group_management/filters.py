from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.functions.del_command import func_del_command
from bot.modules.group_management.pm_error import _pm_error

async def func_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return
    
    await func_del_command(update, context)
    
    db = await global_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_group = db[1]

    filters = find_group.get("filters")

    msg = f"<b><u>Chat filters</u></b>\n\n"
    if filters:
        for keyword in filters:
            msg += f"- <code>{keyword}</code>\n"
    else:
        msg += "- No filters\n"

    await Message.reply_msg(update, msg)
