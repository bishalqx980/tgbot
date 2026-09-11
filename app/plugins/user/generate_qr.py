from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.modules.qr import QR
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "generateqr",
    "commands": ["generateqr", "genqr"], # list of commands including aliases

    "description": "Generate a QR-code-image from text/data/url .! E.g. `/genqr http://google.com`,. OR reply any text/data/url with the command.",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Generate QR", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message

    data = CommandArgs(message.text, message.command) or (re_msg.text or re_msg.caption if re_msg else None)

    if not data:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )

    image_buffer = QR.GenerateQR(data)

    if not image_buffer:
        return await message.reply(
            "Error: Damn not again! I'm not sure what happened!"
        )
    
    await message.reply_photo(
        image_buffer,
        (
            f"**Data:** `{data}`\n"
            f"**Req by:** {user.mention} | `{user.id}`"
        )
    )
