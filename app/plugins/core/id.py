from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import MessageOriginType

from app import bot, COMMAND_PREFIXES


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "id",
    "commands": ["id"], # list of commands including aliases

    "description": "Get CHAT / USER ID,. Reply user with command!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "ID", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    chat = message.chat
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    victim = None
    
    if re_msg:
        forward_origin = re_msg.forward_origin
        from_user = re_msg.from_user

        if forward_origin:
            if forward_origin.type == MessageOriginType.USER:
                victim = forward_origin.sender_user
            elif forward_origin.type == MessageOriginType.CHANNEL:
                victim = forward_origin.chat
        elif from_user:
            victim = from_user
        
        if not victim:
            text = (
                f"• {user.full_name}\n"
                f"  » **ID:** `{user.id}`\n"
                f"• {forward_origin.sender_user_name}\n"
                f"  » **ID:** `Replied user account is hidden!`\n"
                f"• **ChatID:** `{chat.id}`"
            )
        else:
            text = (
                f"• {user.full_name}\n"
                f"  » **ID:** `{user.id}`\n"
                f"• {victim.full_name or victim.title}\n" # this title can cause error (title for channel)
                f"  » **ID:** `{victim.id}`\n"
                f"• **ChatID:** `{chat.id}`"
            )
    else:
        text = (
            f"• {user.full_name}\n"
            f"  » **ID:** `{user.id}`\n"
            f"• **ChatID:** `{chat.id}`"
        )
    
    await message.reply(text)
