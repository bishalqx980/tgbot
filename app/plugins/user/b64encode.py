from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.helpers import CommandArgs
from app.modules.base64 import BASE64


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "encode",
    "commands": ["encode"], # list of commands including aliases

    "description": "Encode text into base64 string! E.g. `/encode aHR0cHM6Ly9iaXNoYWxxeDk4MC5naXRodWIuaW8v` or reply the string with command!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Encode base64", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    text = CommandArgs(message.text, message.command) or (re_msg.text or re_msg.caption if re_msg else None)

    if not text:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    res = BASE64.encode(text)

    await message.reply(
        f"`{res}`" if res else "Error: Huh! I don't know what's going on here..."
    )
