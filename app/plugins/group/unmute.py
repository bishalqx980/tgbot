from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_restrict,
    user_admin,
    user_can_restrict
)
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "unmute",
    "commands": ["unmute", "sunmute", "dunmute"], # list of commands including aliases

    "description": "Unmute chat member! E.g. `/unmute @username reason` or reply a member with `/unmute reason`!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Unmute", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_restrict
@bot_admin
@bot_can_restrict
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    args = CommandArgs(message.text, message.command)

    # priority: @username > reply
    if "@" in args:
        username, _, reason = args.partition(" ")

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
        reason = args
    
    command = message.command[0]
    is_silent = False
    
    try:

        if command.startswith("s"):
            is_silent = True
            await message.delete()
        
        elif command.startswith("d"):
            await bot.delete_messages(
                message.chat.id,
                [
                    message.id,
                    re_msg.id
                ]
            )
        
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
            "Mind blowing. You deserve nobel prize!"
        )
    
    try:

        await message.chat.restrict_member(
            victim.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                # can_send_video_notes=True,
                # can_send_voice_notes=True,
                # can_send_polls=True,
                # can_send_other_messages=True,
                # can_add_web_page_previews=True,
                # can_react_to_messages=True,
                # can_edit_tag=True,
                # can_change_info=True,
                # can_invite_users=True,
                # can_pin_messages=True,
                # can_manage_topics=True,
                # can_send_media_messages=True
            )
        )

        if not is_silent:
            await message.reply_text(
                f"{victim.mention} is unrestricted in this chat." + (f"\nReason: {reason}" if reason else "")
            )
        
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
