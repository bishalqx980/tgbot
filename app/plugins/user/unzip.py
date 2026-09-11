import os
from time import time
from io import BytesIO
from asyncio import sleep
from pathlib import Path

from pyrogram import filters
from pyrogram.types import Message, ReplyParameters, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app import bot, logger, COMMAND_PREFIXES
from app.helpers import CommandArgs, tgProgressUpdater
from app.modules.utils import UTILITY


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "unzip",
    "commands": ["unzip", "uz"], # list of commands including aliases

    "description": "Unzip any `.zip` file. Reply any zip file with this command to unzip the file. E.g. `/unzip password` (if required)",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Unzip", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    password = CommandArgs(message.text, message.command)

    if not re_msg or not re_msg.document:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    if not re_msg.document.file_name.endswith(".zip"):
        return await message.reply(
            "Error: Replied file isn't a `.zip` file!"
        )
    
    """
    Need to add 2GB download limit & need to be private chat only ?
    """

    sent_message = await message.reply("Please wait...")

    try:
        await sent_message.pin(both_sides=True)
    except Exception:
        pass

    # Downloading zip file in memory
    startTime = time()

    zipFile = await re_msg.download(
        re_msg.document.file_name,
        in_memory=False, # Use disk space otherwise it will eat too much RAM
        progress=tgProgressUpdater,
        progress_args=[
            sent_message,
            "📥 Downloading...",
            startTime
        ]
    )

    # Unzipping
    await sent_message.edit_text("🗂️ Unziping...")

    response = UTILITY.unzipFile(zipFile, password)

    if not isinstance(response, list):
        return await sent_message.edit_text(
            f"Error: {response}"
        )
    
    # Uploading the files
    counter = 0
    uploaded = 0
    failed_uploads = []
    document_links = []

    for file in response:
        try:
            counter += 1
            startTime = time()
            percent = counter * 100 / len(response)
            percentBar = UTILITY.createProgressBar(percent)

            statusMessage = (
                "**📤 Uploading...**\n"
                f"**File:** `{file}`\n"
                f"**Progress:** `{percentBar} {percent:.2f}%`"
            )

            document_info = await message.reply_document(
                file,
                reply_parameters=ReplyParameters(
                    message_id=re_msg.id
                ),
                progress=tgProgressUpdater,
                progress_args=[
                    sent_message,
                    statusMessage,
                    startTime
                ]
            )

            if document_info:
                uploaded += 1
                file_name = Path(file).name

                if document_info.link:
                    document_link = f"- [{file_name}]({document_info.link})"
                else:
                    document_link = f"- {file_name}"

                document_links.append(document_link)
            
        except Exception as e:
            file_name = Path(file).name
            failed_uploads.append(f"✘ {e}: `{file_name}`")
        
        await sleep(0.5)

        try:
            os.remove(file)
        except Exception as e:
            logger.error(e)

    text = (
        f"**✅ Upload Completed! ({uploaded}/{len(response)})**\n"
        f"{'\n'.join(document_links)}\n\n"
        f"{'\n'.join(failed_uploads)}"
    )

    try:
        await sent_message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✘ Unpin", "unzip:unpin")
            ]])
        )
    except Exception:
        await sent_message.delete()

        buffer = BytesIO()
        buffer.write(text.encode())
        buffer.seek(0)
        buffer.name = "tmp.md"

        await message.reply_document(buffer)


@bot.on_callback_query(filters.regex(r"^unzip:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):

    query_data = query.data.removeprefix("unzip:")

    if query_data == "unpin":
        await query.answer()

        try:
            await query.message.unpin()
            # remove the unpin button
            await query.message.edit_text(query.message.text.markdown)
        except Exception:
            pass
