async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    with open("log.txt", "rb") as log_file:
        log = log_file.read()
    await Message.send_doc(chat.id, log, "log.txt", "log.txt", e_msg.id)