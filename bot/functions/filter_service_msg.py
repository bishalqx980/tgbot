async def func_filter_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    try:
        await Message.del_msg(chat.id, e_msg)
    except Exception as e:
        logger.error(e)