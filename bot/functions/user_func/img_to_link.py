from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.keyboard_builder import BuildKeyboard
from bot.modules.freeimagehost import upload_image

async def func_imgtolink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message

    if re_msg:
        if re_msg.photo:
            photo = re_msg.photo[-1]
        elif re_msg.document and re_msg.document.mime_type[0:5] == "image":
            photo = re_msg.document
        else:
            photo = None

    if not re_msg or not photo:
        await effective_message.reply_text("Reply a photo to get a public link for that photo!")
        return
    
    sent_message = await effective_message.reply_text(f"💭 Generating...")
    photo = await context.bot.get_file(photo.file_id)

    response = await upload_image(photo.file_path)
    if not response:
        await context.bot.edit_message_text("Timeout! Please try again or report the issue." if response is False else "Oops! Something went wrong!", chat.id, sent_message.id)
        return
    
    image_data = response["image"]

    img_url = image_data.get("url")
    img_width = image_data.get("width")
    img_height = image_data.get("height")
    img_size = image_data.get("size_formatted")
    img_mime = image_data["image"]["mime"]

    text = (
        "↓ <u><b>Image Details</b></u> ↓\n"
        f"<b>- URL:</b> <a href='{img_url}'>◊ See Image ◊</a>\n"
        f"<b>- Width:</b> <code>{img_width}px</code>\n"
        f"<b>- Height:</b> <code>{img_height}px</code>\n"
        f"<b>- Size:</b> <code>{img_size}</code>\n"
        f"<b>- Mime:</b> <code>{img_mime}</code>"
    )

    btn = BuildKeyboard.ubutton([{"View 👀": img_url}])
    await context.bot.edit_message_text(text, chat.id, sent_message.id, reply_markup=btn)
