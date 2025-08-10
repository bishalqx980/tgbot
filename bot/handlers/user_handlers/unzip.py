import os
from io import BytesIO
from asyncio import sleep

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import FileSizeLimit

from bot import logger
from bot.modules.utils import Utils

async def func_unzip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    password = " ".join(context.args) or None

    if not re_msg or not re_msg.document:
        await effective_message.reply_text("Reply any <code>.zip</code> file to extract the file. E.g. <code>/unzip password (if needed)</code>")
        return
    
    if not re_msg.document.file_name.endswith(".zip"):
        await effective_message.reply_text("Replied file isn't a <code>.zip</code> file!")
        return
    
    file_size = re_msg.document.file_size
    if file_size >= FileSizeLimit.FILESIZE_DOWNLOAD:
        await effective_message.reply_text(f"FileSize Error: Replied FileSize {int(file_size / (1024 * 1024))}MB - MaxFileSize Allowed {int(FileSizeLimit.FILESIZE_DOWNLOAD / (1024 * 1024))}MB")
        return
    
    sent_message = await effective_message.reply_text("Please wait...")

    # Reading Zip file in memory
    archive_file = await re_msg.document.get_file()
    zipFile = BytesIO()
    await archive_file.download_to_memory(zipFile)
    zipFile.seek(0)

    # Unzipping
    await sent_message.edit_text("Unziping...")
    response = Utils.unzipFile(zipFile, password)
    if not isinstance(response, list):
        await sent_message.edit_text(f"Error: {response}")
        return
    
    # File path list
    counter = 0
    uploaded = 0
    uploadfailed = ""
    for i in response:
        counter += 1
        try:
            percentBar = Utils.createProgressBar(counter * 100/len(response))
            await sent_message.edit_text((
                "Uploading...\n"
                f"File: <code>{i}</code>\n"
                f"Percent: <code>{percentBar}</code>"
            ))
            await effective_message.reply_document(i)
            uploaded += 1
        except Exception as e:
            uploadfailed += f"- {e}: <code>{i}</code>\n"
        
        await sleep(0.5)

        try:
            os.remove(i)
        except Exception as e:
            logger.error(e)
    
    await sent_message.edit_text(f"Upload Completed! ({uploaded}/{len(response)})\n{uploadfailed}")
