from time import time
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from bot.modules.qr import QR

async def func_decqr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message

    if not re_msg or not (re_msg.photo or re_msg.document):
        await effective_message.reply_text("Reply a QR code image using /decqr to decode it!")
        return
    
    if re_msg.document and not "image" in re_msg.document.mime_type:
        await effective_message.reply_text("Replied message isn't an image!")
        return
    
    image = re_msg.photo or re_msg.document
    if isinstance(image, tuple): image = image[-1]
    
    if re_msg.photo:
        sent_message = await effective_message.reply_photo(image.file_id, "Please wait...")
    else:
        sent_message = await effective_message.reply_document(image.file_id, "Please wait...")

    # Reading Image file in memory
    image_data = await image.get_file()
    imageFile = BytesIO()
    await image_data.download_to_memory(imageFile)
    imageFile.seek(0)

    start_time = time()
    response = QR.decode_qr(imageFile)
    response_time = f"{((time() - start_time) * 1000):.2f}ms"

    if response:
        text = (
            f"<b>Decoded Data:</b> <code>{response.data.decode()}</code>\n"
            f"<b>Type:</b> <code>{response.type}</code>\n"
            f"<b>R.time:</b> <code>{response_time}</code>\n"
            f"<b>Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
        )
    else:
        text = "Oops! Something went wrong!"

    await sent_message.edit_caption(text)
