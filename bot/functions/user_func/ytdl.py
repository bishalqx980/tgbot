import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.ytdlp import youtube_download

async def func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    url = " ".join(context.args)

    if not url or not url.startswith("http"):
        await effective_message.reply_text("Download audio/song from youtube. E.g. <code>/ytdl url</code>")
        return
    
    sent_message = await effective_message.reply_text("Downloading...")

    response = youtube_download(url)
    if not response:
        await context.bot.edit_message_text("Oops! Something went wrong!", chat.id, sent_message.id)
        return
    
    file_name = f"{response['file_name']}.mp3"
    
    await context.bot.delete_message(chat.id, sent_message.id)
    await effective_message.reply_audio(response["file_path"], title=file_name, filename=file_name)

    try:
        os.remove(response["file_path"])
    except Exception as e:
        logger.error(e)
