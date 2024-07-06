from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.pastebin import PASTEBIN

async def func_paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    text = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not text:
        await Message.reply_msg(update, "Use <code>/paste text</code> or reply the message with <code>/paste</code>!")
        return

    sent_msg = await Message.reply_msg(update, f"Creating...")
    paste = await PASTEBIN.create(text)
    if paste == False:
        msg = "pastebin_api not found!"
    elif paste:
        msg = paste
    elif not paste:
        msg = "An error occured..."

    await Message.edit_msg(update, msg, sent_msg)
