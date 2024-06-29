from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.base64 import BASE64

async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if not msg and not re_msg:
        await Message.reply_msg(update, "Use <code>/encode the `Decoded` or `normal` text</code>\nor reply the `Decoded` or `normal` text with <code>/encode</code>\nE.g. <code>/encode the `Decoded` or `normal` text you want to encode</code>")
        return

    if not msg and re_msg:
        msg = re_msg.text or re_msg.caption
    
    encode = await BASE64.encode(msg)
    msg = f"<code>{encode}</code>" if encode else "Invalid text!"
    await Message.reply_msg(update, msg)
