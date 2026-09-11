from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.modules import telegraph
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "telegraph",
    "commands": ["paste", "telegraph", "graph"], # list of commands including aliases

    "description": "Host any text / code on telegraph server! Reply the text with command OR E.g. `/paste text`",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Telegraph", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    text = (re_msg.text.html or re_msg.caption.html) if re_msg else CommandArgs(message.text, message.command)

    if not text:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    sent_message = await message.reply("📦 Processing...")

    response = await telegraph.paste(text, f"{user.full_name}-({user.id})-")

    if not response:
        return await sent_message.edit_text(
            "Error: Huh? What? What's going on here?"
        )
    
    await sent_message.edit_text(
        "**Page has created successfully!!**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Visit", url=response),
            InlineKeyboardButton("Copy Link", copy_text=response)
        ]])
    )
