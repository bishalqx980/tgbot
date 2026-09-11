from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_restrict
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "kickme",
    "commands": ["kickme", "leavemealone", "byeforever"], # list of commands including aliases

    "description": "Kick yourself from group chat! Try at your own risk!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Kickme", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@bot_admin
@bot_can_restrict
async def func_(_, message: Message):
    user_id = message.from_user.id

    # check if user if admin
    try:

        chat_user_data = await message.chat.get_member(
            user_id
        )

        if chat_user_data.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]:
            return await message.reply_text(
                "UwU >.< , I'm not going to kick you! You're tied with everyone."
            )
        
    except Exception as e:
        logger.error(e)
        return await message.reply_text(
            f"Error: {e}"
        )

    try:

        # ban for 1min then, they can rejoin
        until_date = datetime.now() + timedelta(minutes=1)

        await message.chat.ban_member(
            user_id,
            until_date=until_date
        )

        await message.reply_text(
            f"Good choice! Get out of my sight, {message.from_user.mention}."
        )

    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
