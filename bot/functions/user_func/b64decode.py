from telegram import Update
from telegram.ext import ContextTypes
from ...modules.base64 import BASE64

async def func_decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None) 

    if not text:
        await effective_message.reply_text("Use <code>/decode base64code</code>\nor reply the base64code with <code>/decode</code> command.")
        return
    
    decoded_text = BASE64.decode(text)
    await effective_message.reply_text(f"<code>{decoded_text}</code>" if decoded_text else "Invalid base64!")
