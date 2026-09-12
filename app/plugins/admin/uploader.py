import os
from time import time

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, sudo_required
from app.helpers import CommandArgs, tgProgressUpdater


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "upload",
    "commands": ["upload", "ul"], # list of commands including aliases

    "description": "Upload a file from host! E.g. `/upload path`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Upload", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@sudo_required
async def func_(_, message: Message):
    args = CommandArgs(message.text, message.command)
    if not args:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    sent_message = await message.reply("Uploading...")

    try:

        startTime = time()
        filename = os.path.basename(args)

        r = await message.reply_document(
            open(args, "rb"),
            caption=(
                "**Upload completed!**\n\n"
                f"**File name** : `{filename}`\n"
                f"**File path** : `{args}`"
            ),
            file_name=filename,
            progress=tgProgressUpdater,
            progress_args=(sent_message, "Uploading...", startTime)
        )

        if r:
            await sent_message.delete()
    
    except Exception as e:
        await sent_message.edit_text(f"Error: {e}")
