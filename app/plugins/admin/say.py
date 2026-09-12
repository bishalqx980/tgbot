from pyrogram import filters
from pyrogram.types import Message, ReplyParameters

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import sudo_required
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "say",
    "commands": ["say"], # list of commands including aliases

    "description": "Send a message for the bot to repeat! E.g. `/say What's Up!`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Say", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@sudo_required
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    speech = CommandArgs(message.text, message.command) # the sentence to say
    
    try:
        await message.delete()
    except Exception as e:
        return await message.reply(f"Error: {e}")
    
    if not speech:
        try:
            return await bot.send_message(
                user.id,
                f"**Name :** `{__module__['name']}`\n"
                f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
                f"**Description :** <i>{__module__['description']}</i>\n\n"

                f"**Version :** `{__module__['version']}`\n"
                f"**Author :** `{__module__['author']}`\n\n"

                f"#{__module__['_id']}"
            )
        except Exception as e:
            logger.error(e)
            return
    
    await message.reply(
        speech,
        reply_parameters=ReplyParameters(
            message_id=re_msg.id if re_msg else None
        )
    )
