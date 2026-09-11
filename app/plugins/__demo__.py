from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "demo",
    "commands": ["demo"], # list of commands including aliases

    "description": "This is a demo command!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Demo", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat

    await message.reply(
        f"**Name :** `{__module__['name']}`\n"
        f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
        f"**Description :** <i>{__module__['description']}</i>\n\n"

        f"**Version :** `{__module__['version']}`\n"
        f"**Author :** `{__module__['author']}`\n\n"

        f"#{__module__['_id']}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Click", "demo:hello")
        ]])
    )


@bot.on_callback_query(filters.regex(r"^demo:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    if query.data == "demo:hello":
        await query.answer("Hi, How are you!", True)
