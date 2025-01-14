import time
import asyncio
import subprocess
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    command = " ".join(context.args)
    command = command.replace("'", "")

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_message(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not command:
        await Message.reply_message(update, "Use <code>/shell dir/ls</code> [linux/Windows Depend on your hosting server]")
        return
    
    sent_msg = await Message.reply_message(update, "<b>⌊ please wait... ⌉</b>")
    
    time_executing = time.time()

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        logger.error(e)
        return
    
    time_executed = time.time()
    
    if not result.stdout and not result.stderr:
        await Message.edit_message(update, "<b>⌊ None ⌉</b>", sent_msg)
        return
    
    response = None

    msg = result.stdout if result.stdout else result.stderr
    response = await Message.edit_message(update, f"<pre>{msg}</pre>", sent_msg)
    if not response:
        try:
            open("sys/shell.txt", "w").write(msg)
            shell = open("sys/shell.txt", "rb").read()
        except Exception as e:
            logger.error(e)
            await Message.edit_message(update, e, sent_msg)
            return
        
        await Message.delete_message(chat.id, sent_msg)
        await Message.send_document(chat.id, shell, "shell.txt", f"<b>Command</b>: {command}\n<b>Execute time</b>: {(time_executed - time_executing):.2f}s", reply_message_id=e_msg.id)
