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
    "name": "mute",
    "commands": ["mute", "smute", "dmute"], # list of commands including aliases

    "description": "Mute chat member! E.g. `/mute @username reason` or reply a member with `/mute reason`!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Mute", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

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
            "Nice try kiddo. I'm not falling for that one."
        )
    
    try:

        await message.chat.restrict_member(
            victim.id,
            ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                # can_send_video_notes=False,
                # can_send_voice_notes=False,
                # can_send_polls=False,
                # can_send_other_messages=False,
                # can_add_web_page_previews=False,
                # can_react_to_messages=False,
                # can_edit_tag=False,
                # can_change_info=False,
                # can_invite_users=False,
                # can_pin_messages=False,
                # can_manage_topics=False,
                # can_send_media_messages=False
            )
        )

        if not is_silent:
            await message.reply_text(
                f"{victim.mention} is restricted in this chat." + (f"\nReason: {reason}" if reason else "")
            )
        
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
