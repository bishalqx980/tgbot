import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.qr import QR

async def func_gen_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    data = " ".join(context.args)

    if not data:
        await Message.reply_msg(update, "Use <code>/qr url/data/text</code> to generate a QR code img...\nE.g. <code>/qr https://google.com</code>")
        return

    sent_msg = await Message.reply_msg(update, f"Generating...")
    gen_qr = await QR.gen_qr(data)

    if not gen_qr:
        await Message.edit_msg(update, "Something went wrong!", sent_msg)
        return

    try:
        await Message.send_img(chat.id, gen_qr, data)
        os.remove(gen_qr)
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(e)
