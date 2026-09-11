from uuid import uuid4
from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, admin_require
from app.helpers import CommandArgs
from app.modules.shell import RunCommand


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "bash",
    "commands": ["bash", "shell", "cmd"], # list of commands including aliases

    "description": "Run any command on CMD! E.g. `/bash whoami`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Bash/Shell/CMD", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@admin_require
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
    
    sent_message = await message.reply("Please wait...")

    shell = RunCommand(args)

    if not shell:
        return await sent_message.edit_text("Error: please check /log !!")
    
    result = shell.get("stdout") or shell.get("stderr")

    try:
        await sent_message.edit_text(
            f"**$** `{args}`\n\n"
            f"<pre>{result}</pre>"
        )
    except:
        buffer = BytesIO(result.encode())
        buffer.name = f"{args}-{uuid4().hex}.txt"

        await sent_message.delete()

        await message.reply_document(
            buffer,
            caption=(
                f"**$** `{args}`\n\n"
                f"<i>{buffer.name}</i>"
            ),
            file_name=buffer.name
        )
