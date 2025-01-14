import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.ytdlp import youtube_download

async def func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    url = " ".join(context.args)

    if not url or not url.startswith("http"):
        await Message.reply_message(update, "Download audio/song from youtube. E.g. <code>!ytdl url</code>")
        return
    
    sent_msg = await Message.reply_message(update, "Downloading...")
    response = await youtube_download(url)

    if not response:
        await Message.edit_message(update, "Oops, something went wrong...", sent_msg)
        return
    
    await Message.send_audio(chat.id, response["file_path"], f"{response['file_name']}.mp3", response['file_name'], reply_message_id=e_msg.id)
    await Message.delete_message(chat.id, sent_msg)

    try:
        os.remove(response["file_path"])
    except Exception as e:
        logger.error(e)
