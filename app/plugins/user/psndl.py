from urllib.parse import quote

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES, PSNDL_WEBSITE_URL
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "psndl",
    "commands": ["psndl"], # list of commands including aliases

    "description": "Search for PS3 Games package download link! E.g. `/psndl uncharted`",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "PSNDL", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    game_name = CommandArgs(message.text, message.command)

    if not game_name:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Website", url=PSNDL_WEBSITE_URL)
            ]])
        )
    
    await message.reply(
        f"**📑 Search result for {game_name}**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            "Visit",
            url=f"{PSNDL_WEBSITE_URL}?name={quote(game_name)}"
        )]])
    )
