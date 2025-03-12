import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.functions.sudo_users import _power_users

async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = fetch_sudos()
    if user.id not in power_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    log = open("sys/log.txt", "rb").read()
    date_time = datetime.now()

    await Message.send_document(user.id, log, "log.txt", date_time.strftime("%d-%m-%Y %H:%M:%S"))
