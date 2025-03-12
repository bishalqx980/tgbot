from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.base64 import BASE64

async def func_encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None) 

    if not text:
        await effective_message.reply_text("Use <code>/encode text</code>\nor reply any text with <code>/encode</code> command.")
        return
    
    encoded_text = BASE64.encode(text)
    await effective_message.reply_text(f"<code>{encoded_text}</code>" if encoded_text else "Invalid text!")
