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
        await Message.reply_msg(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        del_msg_ids = [e_msg.id, e_msg.id + 1]
        await asyncio.gather(*(Message.del_msg(chat.id, msg_id=msg_id) for msg_id in del_msg_ids))
        return
    
    if not command:
        await Message.reply_msg(update, "E.g. <code>/shell dir/ls</code> [linux/Windows Depend on your hosting device]")
        return
    
    sent_msg = await Message.reply_msg(update, "<b>⌊ please wait... ⌉</b>")
    
    time_executing = time.time()

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        logger.error(e)
        return
    
    time_executed = time.time()
    
    if not result.stdout and not result.stderr:
        await Message.edit_msg(update, "<b>⌊ None ⌉</b>", sent_msg)
        return
    
    response = None

    msg = result.stdout if result.stdout else result.stderr
    response = await Message.edit_msg(update, f"<pre>{msg}</pre>", sent_msg)
    if not response:
        try:
            open('shell.txt', 'w').write(msg)
            shell = open("shell.txt", "rb").read()
        except Exception as e:
            logger.error(e)
            await Message.edit_msg(update, e, sent_msg)
            return
        
        await Message.send_doc(chat.id, shell, "shell.txt", f"<b>Command</b>: {command}\n<b>Execute time</b>: {(time_executed - time_executing):.2f}s", e_msg.id)
        await Message.del_msg(chat.id, sent_msg)
