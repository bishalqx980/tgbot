from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_pin_messages,
    user_admin,
    user_can_pin_messages
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "pin",
    "commands": ["pin", "spin"], # list of commands including aliases

    "description": "Pin replied message silently or loudly. E.g. `/spin` for silent pin & `/pin` for loud pin.",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Pin", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_pin_messages
@bot_admin
@bot_can_pin_messages
async def func_(_, message: Message):
    re_msg = message.reply_to_message

    command = message.command[0]
    is_silent = False
    
    try:

        if command.startswith("s"):
            is_silent = True
            await message.delete()
        
    except:
        pass
    
    if not re_msg:
        return await message.reply_text(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    try:

        await re_msg.pin(disable_notification=is_silent)

        if not is_silent:
            await message.reply_text(
                f"Message [{re_msg.id}]({re_msg.link}) is pinned {'silently' if is_silent else 'loudly'} in this chat by {message.from_user.mention if message.from_user else 'Anonymous'}."
            )
        
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
