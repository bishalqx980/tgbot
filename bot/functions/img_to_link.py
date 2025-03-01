from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.freeimagehost import upload_image


async def func_img_to_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    re_msg = update.message.reply_to_message
    if re_msg:
        if re_msg.photo:
            photo = re_msg.photo[-1]
        elif re_msg.document and re_msg.document.mime_type[0:5] == "image":
            photo = re_msg.document
        else:
            photo = None

    if not re_msg or not photo:
        await Message.reply_message(update, "Reply a photo to get a public link for that photo!")
        return
    
    sent_msg = await Message.reply_message(update, f"💭 Generating...")
    photo = await bot.get_file(photo.file_id)

    itl = await upload_image(photo.file_path)
    if not itl:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
        return
    
    if itl[0] == False:
        await Message.edit_message(update, f"Timeout! Please try again or report the issue.", sent_msg)
        return
    
    image_data = itl[1]["image"]

    img_url = image_data.get("url")
    img_width = image_data.get("width")
    img_height = image_data.get("height")
    img_size = image_data.get("size_formatted")
    img_mime = image_data["image"]["mime"]

    msg = (
        "↓ <u><b>Image Details</b></u> ↓\n"
        f"<b>- URL:</b> <a href='{img_url}'>◊ See Image ◊</a>\n"
        f"<b>- Width:</b> <code>{img_width}px</code>\n"
        f"<b>- Height:</b> <code>{img_height}px</code>\n"
        f"<b>- Size:</b> <code>{img_size}</code>\n"
        f"<b>- Mime:</b> <code>{img_mime}</code>"
    )

    btn = await Button.ubutton({"View 👀": img_url})
    await Message.edit_message(update, msg, sent_msg, btn)
