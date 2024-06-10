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
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if not command:
        await Message.reply_msg(update, "E.g. <code>/shell dir/ls</code> [linux/Windows Depend on your hosting device]")
        return
    
    sent_msg = await Message.reply_msg(update, "<b>⌊ please wait...⌉</b>")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        logger.error(e)
    
    if not result.stdout and not result.stderr:
        await Message.edit_msg(update, "<b>⌊ None ⌉</b>", sent_msg)
        return
    
    response = None

    msg = result.stdout if result.stdout else result.stderr
    response = await Message.edit_msg(update, f"<pre>{msg}</pre>", sent_msg)
    if not response:
        try:
            with open('shell.txt', 'w') as shell_file:
                shell_file.write(msg)
            with open("shell.txt", "rb") as shell_file:
                shell = shell_file.read()
            await Message.send_doc(chat.id, shell, "shell.txt", command, e_msg.id)
            await Message.del_msg(chat.id, sent_msg)
        except Exception as e:
            logger.error(e)
