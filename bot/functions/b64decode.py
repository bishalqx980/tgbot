from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.base64 import BASE64

async def func_b64decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None) 

    if not msg:
        await Message.reply_msg(update, "Use <code>/decode 'base64-text'</code>\nor reply the 'base64-text' with <code>/decode</code> command.")
        return
    
    decode = await BASE64.decode(msg)
    msg = f"<code>{decode}</code>" if decode else "Invalid base64!"
    await Message.reply_msg(update, msg)
