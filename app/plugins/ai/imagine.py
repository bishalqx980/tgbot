from time import time

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.helpers import CommandArgs
from app.modules import llm


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "aiimagine",
    "commands": ["imagine", "photogen"], # list of commands including aliases

    "description": "Generate A.I. image using promt! E.g. `/imagine A dog is playing on the moon.`",
    "category": "ai", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Imagine / AI", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    prompt = CommandArgs(message.text, message.command)
    
    if not prompt:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    sent_message = await message.reply("🎨 Generating...")
    
    start_time = time()
    response = await llm.imagine(prompt)
    response_time = int(time() - start_time)

    if not response:
        return await sent_message.edit_text(
            "Error: Ohh I'm feeling sleepy, I can't imagine right now..."
        )
    
    caption = (
        f"> {user.mention} : {prompt}\n"
        f"**Process time:** `{response_time}`\n"
        f"**UserID:** `{user.id}`"
    )

    await sent_message.delete()
    await message.reply_photo(response, caption)
