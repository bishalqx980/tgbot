import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.qr import QR

async def func_gen_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    re_msg = update.message.reply_to_message
    data = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not data:
        await Message.reply_message(update, "Use <code>/qr url/data/text</code> to generate a QR code image.\nor reply the 'url/data/text' with <code>/qr</code> command.\nE.g. <code>/qr https://google.com</code>")
        return

    sent_msg = await Message.reply_message(update, f"Generating...")
    gen_qr = await QR.gen_qr(data)

    if not gen_qr:
        await Message.edit_message(update, "Oops, something went wrong...", sent_msg)
        return
    
    await Message.send_image(chat.id, gen_qr, data, re_msg.id if re_msg else None)
    await Message.delete_message(chat.id, sent_msg)

    # Remove the image from storage
    try:
        os.remove(gen_qr)
    except Exception as e:
        logger.error(e)
