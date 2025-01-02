from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.base64 import BASE64

async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None) 

    if not msg:
        await Message.reply_msg(update, "Use <code>/encode 'text'</code>\nor reply any text with <code>/encode</code> command.")
        return
    
    encode = await BASE64.encode(msg)
    msg = f"<code>{encode}</code>" if encode else "Invalid text!"
    await Message.reply_msg(update, msg)
