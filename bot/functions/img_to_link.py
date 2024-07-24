import os
import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.telegraph import TELEGRAPH


async def func_img_to_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    if re_msg:
        photo = re_msg.photo[-1] if re_msg.photo else None

    if not re_msg or not photo:
        await Message.reply_msg(update, "Reply a photo to get a public link for that photo!")
        return
    
    sent_msg = await Message.reply_msg(update, f"Generating public link...")
    photo = await bot.get_file(photo.file_id)
    dir_name = "download"
    os.makedirs(dir_name, exist_ok=True)
    f_name = f"{dir_name}/image.png"
    req = requests.get(photo.file_path)
    open(f_name, "wb").write(req.content)
    
    itl = await TELEGRAPH.upload_img(f_name)
    if not itl:
        await Message.edit_msg(update, "Oops, something went wrong...", sent_msg)
        return
    
    await Message.edit_msg(update, itl, sent_msg)

    try:
        os.remove(f_name)
    except Exception as e:
        logger.error(e)
