import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users

async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_message(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    log = open("sys/log.txt", "rb").read()
    date_time = datetime.now()

    await Message.send_document(user.id, log, "log.txt", date_time.strftime("%d-%m-%Y %H:%M:%S"))
