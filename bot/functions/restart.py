import os
import sys
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users
from bot.modules.database.mongodb import MongoDB


async def func_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "Check pm!")
    
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    if not bot_status or bot_status == "alive":
        await Message.send_msg(user.id, "Restaring...")
        await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "restart")
        try:
            os.execv(sys.executable, ["python"] + sys.argv)
        except Exception as e:
            logger.error(e)
    elif bot_status == "restart":
        await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
        await Message.send_msg(user.id, "Bot Restarted!")  
