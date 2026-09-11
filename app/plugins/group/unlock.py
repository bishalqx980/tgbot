from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_manage_chat,
    user_admin,
    user_can_manage_chat
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "chatunlock",
    "commands": ["unlock", "chatunlock"], # list of commands including aliases

    "description": "Unlock the chat, normalize the chat!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Chat Unlock", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_manage_chat
@bot_admin
@bot_can_manage_chat
async def func_(_, message: Message):

    try:

        await bot.set_chat_permissions(
            message.chat.id,
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

        await message.reply_text(
            f"Chat has been unlocked by {message.from_user.mention if message.from_user else 'Anonymous'}."
        )
    
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
