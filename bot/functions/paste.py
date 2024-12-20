from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.pastebin import PASTEBIN

async def func_paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    re_msg = update.message.reply_to_message
    text = re_msg.text or re_msg.text if re_msg else " ".join(context.args)

    if not text:
        await Message.reply_msg(update, "Use <code>/paste text</code> or reply the message with <code>/paste</code>!")
        return

    sent_msg = await Message.reply_msg(update, f"Creating...")
    # paste = await TELEGRAPH.paste(text.replace("\n", "<br>"), user.full_name)
    paste = await PASTEBIN.create(text, f"{user.full_name} | {user.id}")
    if not paste:
        await Message.edit_msg(update, "Oops, something went wrong...", sent_msg)
        return

    await Message.edit_msg(update, paste, sent_msg)
