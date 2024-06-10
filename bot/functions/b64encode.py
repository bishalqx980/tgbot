async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if not msg:
        if re_msg:
            msg = re_msg.text or re_msg.caption
        else:
            await Message.reply_msg(update, "Use <code>/encode the `Decoded` or `normal` text</code>\nor reply the `Decoded` or `normal` text with <code>/encode</code>\nE.g. <code>/encode the `Decoded` or `normal` text you want to encode</code>")
            return
    
    encode = await BASE64.encode(msg)
    if encode:
        await Message.reply_msg(update, f"<code>{encode}</code>")
    else:
        await Message.reply_msg(update, f"Invalid text!")