from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.modules.utils import UTILITY
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "calculator",
    "commands": ["calculate", "calc"], # list of commands including aliases

    "description": "Calculate some math! E.g. `/calc 123 + 78 * 15 / 3` or reply the math with command!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Calculator", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

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
    
    res = UTILITY.calculator(text)

    await message.reply(
        "> **Calculator**\n\n"
        f"**Result :** <i>{res}</i>"
    )
