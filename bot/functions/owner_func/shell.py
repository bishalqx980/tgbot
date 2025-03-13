import asyncio
import subprocess
from time import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.sudo_users import fetch_sudos

async def func_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    command = " ".join(context.args)
    command = command.replace("'", "")

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    if not command:
        await effective_message.reply_text("Use <code>/shell dir/ls</code> [linux/Windows Depend on your hosting server]")
        return
    
    sent_message = await effective_message.reply_text("<b>⌊ please wait... ⌉</b>")
    
    time_executing = time()

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        logger.error(e)
        return
    
    time_executed = time()
    
    if not result.stdout and not result.stderr:
        await context.bot.edit_message_text("<b>⌊ None ⌉</b>", chat.id, sent_message.id)
        return

    result = result.stdout if result.stdout else result.stderr

    try:
        await context.bot.edit_message_text(f"<pre>{result}</pre>", chat.id, sent_message.id)
    except:
        try:
            open("sys/shell.txt", "w").write(result)
            shell = open("sys/shell.txt", "rb").read()
        except Exception as e:
            logger.error(e)
            await context.bot.edit_message_text(str(e), chat.id, sent_message.id)
            return
        
        await context.bot.delete_message(chat.id, sent_message.id)
        await effective_message.reply_document(shell, f"<b>Command</b>: {command}\n<b>Execute time</b>: {(time_executed - time_executing):.2f}s", filename="shell.txt")
