from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.modules.api.shrinkme import ShortURL
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "shortener",
    "commands": ["shortener", "shortit", "shorturl", "shrinkme"], # list of commands including aliases

    "description": "Short any URL / Link! Reply any link OR E.g. `/shorturl http://google.com`",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "URL Shortener", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    url = (re_msg.text or re_msg.caption) if re_msg else CommandArgs(message.text, message.command)

    if not url:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    if url[0:4] != "http":
        url = f"http://{url}"
    
    shortened_url = await ShortURL(url)
    await message.reply(shortened_url if shortened_url else "Error: Don't know what just happened! But something isn't good.")
