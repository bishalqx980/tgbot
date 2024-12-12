from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message
from bot.modules.imgbb import imgbb_upload


async def func_img_to_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    re_msg = update.message.reply_to_message
    if re_msg:
        photo = re_msg.photo[-1] if re_msg.photo else None

    if not re_msg or not photo:
        await Message.reply_msg(update, "Reply a photo to get a public link for that photo!")
        return
    
    sent_msg = await Message.reply_msg(update, f"Generating public link...")
    photo = await bot.get_file(photo.file_id)

    itl = await imgbb_upload(photo.file_path, user.id)
    if itl == False:
        await Message.edit_msg(update, "imgbb_api not found!", sent_msg)
        return

    if not itl:
        await Message.edit_msg(update, "Oops, something went wrong...", sent_msg)
        return
    
    itl_data = itl.get("data")
    img_url = itl_data.get("url") # actual image
    img_display_url = itl_data.get("display_url") # preview image
    img_width = itl_data.get("width")
    img_height = itl_data.get("height")
    img_size = itl_data.get("size")

    caption_msg = (
        "↓ <u><b>Image Details</b></u> ↓\n"
        f"<b>- URL:</b> <a href='{img_url}'>◊ See Image ◊</a>\n"
        f"<b>- Width:</b> <code>{img_width}px</code>\n"
        f"<b>- Height:</b> <code>{img_height}px</code>\n"
        f"<b>- Size:</b> <code>{(img_size / 1024 / 1024):.2f} MB</code>\n\n"
        f"<code>{img_url}</code>"
    )

    await Message.send_img(chat.id, img_display_url, caption_msg)
    await Message.del_msg(chat.id, sent_msg)
