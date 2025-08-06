import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.ytdlp import youtube_download

async def func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    url = " ".join(context.args)

    if not url or not url.startswith("http"):
        await effective_message.reply_text("Download audio/song from youtube. E.g. <code>/ytdl url</code>")
        return
    
    sent_message = await effective_message.reply_text("Downloading...")

    response = youtube_download(url)
    if not isinstance(response, dict):
        await sent_message.edit_text(f"Error: {response}")
        return
    
    file_name = f"{response['title']}.mp3"
    file_path = response["file_path"]

    try:
        await effective_message.reply_audio(file_path, title=file_name, filename=file_name)
        await sent_message.delete()
    except Exception as e:
        await sent_message.edit_text(str(e))
        return
    
    try:
        os.remove(response["file_path"])
    except Exception as e:
        logger.error(e)
