from time import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.qr import QR

async def func_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    data = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not data:
        await effective_message.reply_text("Use <code>/qr url/data/text</code> to generate a QR code.\nor reply the 'url/data/text' with <code>/qr</code> command.\nE.g. <code>/qr https://google.com</code>")
        return

    start_time = time()
    response = QR.generate_qr(data)
    response_time = f"{((time() - start_time) * 1000):.2f}ms"

    if not response:
        await effective_message.reply_text("Oops! Something went wrong!")
        return
    
    caption = (
        f"<b>Data:</b> <code>{data}</code>\n"
        f"<b>R.time:</b> <code>{response_time}</code>\n"
        f"<b>Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
    )

    await effective_message.reply_photo(response, caption)
