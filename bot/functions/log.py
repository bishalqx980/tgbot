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
        await Message.reply_msg(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        del_msg_ids = [e_msg.id, e_msg.id + 1]
        await asyncio.gather(*(Message.del_msg(chat.id, msg_id=msg_id) for msg_id in del_msg_ids))
        return
    
    log = open("log.txt", "rb").read()
    date_time = datetime.now()

    await Message.send_doc(user.id, log, "log.txt", date_time.strftime("%d-%m-%Y %H:%M:%S"))
