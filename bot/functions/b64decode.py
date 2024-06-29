from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.base64 import BASE64

async def func_b64decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if not msg and not re_msg:
        await Message.reply_msg(update, "Use <code>/decode the `Encoded` text</code>\nor reply the `Encoded` text with <code>/decode</code>\nE.g. <code>/decode the `Encoded` text you want to decode</code>")
        return

    if not msg and re_msg:
        msg = re_msg.text or re_msg.caption
    
    decode = await BASE64.decode(msg)
    msg = f"<code>{decode}</code>" if decode else "Invalid base64!"
    await Message.reply_msg(update, msg)
