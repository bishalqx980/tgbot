import os
import time
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.qr import QR

async def func_gen_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    e_msg = update.effective_message
    data = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not data:
        await Message.reply_message(update, "Use <code>/qr url/data/text</code> to generate a QR code.\nor reply the 'url/data/text' with <code>/qr</code> command.\nE.g. <code>/qr https://google.com</code>")
        return

    sent_msg = await Message.reply_message(update, f"📝 Generating...")
    start_time = time.time()
    response = await QR.generate_qr(data, f"qrcode_{user.id}")
    response_time = int((time.time() - start_time) * 1000)

    if not response:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
        return
    
    caption = (
        f"<b>📝 Data:</b> <code>{data}</code>\n"
        f"<b>⏳ R.time:</b> <code>{response_time}ms</code>\n"
        f"<b>🗣 Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
    )
    
    reply_message_id = re_msg.id if re_msg else e_msg.id
    await Message.send_image(chat.id, response, caption, reply_message_id)
    await Message.delete_message(chat.id, sent_msg)

    # Remove the image from storage
    try:
        os.remove(response)
    except Exception as e:
        logger.error(e)
