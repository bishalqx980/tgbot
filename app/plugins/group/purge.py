from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_delete_messages,
    user_admin,
    user_can_delete_messages
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "purge",
    "commands": ["purge", "spurge", "del", "sdel"], # list of commands including aliases

    "description": "Purge all messages from the replied-to message onward.",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Purge", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_delete_messages
@bot_admin
@bot_can_delete_messages
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

    sent_message = await message.reply(
        "Message purge process is started!"
    )
    
    try:

        message_ids = []
        for message_id in range(re_msg.id, message.id + 1):
            message_ids.append(message_id)

        if is_silent:
            message_ids.append(sent_message.id)
        
        await bot.delete_messages(
            message.chat.id,
            message_ids
        )

        if not is_silent:
            await sent_message.edit_text(
                f"Message purge process has been completed."
            )
        
    except Exception as e:
        return await sent_message.edit_text(
            f"Error: {e}"
        )
