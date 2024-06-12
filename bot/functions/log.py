import time
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users

async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        _bot_info = await bot.get_me()
        await Message.reply_msg(update, f"<a href='https://t.me/{_bot_info.username}'>Sent in your pm boss!</a>")
    
    with open("log.txt", "rb") as log_file:
        log = log_file.read()
    
    await Message.send_doc(user.id, log, "log.txt", time.time())
