from telegram import Update
from telegram.ext import ContextTypes
from ...modules import telegraph

async def func_paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = (re_msg.text_html or re_msg.caption_html) if re_msg else " ".join(context.args)

    if not text:
        await effective_message.reply_text("Use <code>/paste text</code> or reply the message/text with <code>/paste</code> command.")
        return

    sent_message = await effective_message.reply_text(f"Creating...")

    paste = await telegraph.paste(text, user.full_name)
    if not paste:
        await context.bot.edit_message_text("Oops! Something went wrong!", chat.id, sent_message.id)
        return
    
    await context.bot.edit_message_text(paste, chat.id, sent_message.id)
