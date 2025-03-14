from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.telegraph import TELEGRAPH

async def func_paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    re_msg = update.message.reply_to_message
    text = (re_msg.text_html or re_msg.caption_html) if re_msg else " ".join(context.args)

    if not text:
        await Message.reply_message(update, "Use <code>/paste text</code> or reply the message/text with <code>/paste</code> command.")
        return

    sent_msg = await Message.reply_message(update, f"Creating...")
    paste = await TELEGRAPH.paste(text.replace("\n", "<br>"), user.full_name)
    if not paste:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
        return

    await Message.edit_message(update, paste, sent_msg)
