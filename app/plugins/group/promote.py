from pyrogram import filters
from pyrogram.types import Message, ChatAdministratorRights

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_promote,
    user_admin,
    user_can_promote
)
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "promote",
    "commands": ["promote", "spromote"], # list of commands including aliases

    "description": "Promote chat member! E.g. `/promote @username title` or reply a member with `/promote title`!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Promote", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_promote
@bot_admin
@bot_can_promote
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    args = CommandArgs(message.text, message.command)

    # priority: @username > reply
    if "@" in args:
        username, _, title = args.partition(" ")

        # Extra useless work ?
        try:

            info = await message.chat.get_member(username)
            victim = info.user

        except Exception as e:
            return await message.reply_text(
                f"Error: {e}"
            )

    else:
        victim = re_msg.from_user if re_msg else None
        title = args
    
    command = message.command[0]
    is_silent = False
    
    try:

        if command.startswith("s"):
            is_silent = True
            await message.delete()
        
    except:
        pass
    
    if not victim:
        return await message.reply_text(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    if victim.id == bot.me.id:
        return await message.reply_text(
            "Hmm, I wish I could give myself more power!"
        )
    
    try:
        
        await message.chat.promote_member(
            victim.id,
            ChatAdministratorRights(
                can_invite_users=True
            )
        )

        await bot.set_administrator_title(
            message.chat.id,
            victim.id,
            title
        )

        if not is_silent:
            await message.reply_text(
                f"{victim.mention} is promoted to admin in this chat." + (f"\nTitle: {title}" if title else "")
            )
    
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
