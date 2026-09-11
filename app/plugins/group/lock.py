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
    "name": "chatlock",
    "commands": ["lock", "chatlock", "lockdown"], # list of commands including aliases

    "description": "Lockdown the chat, No one can send message etc. except admin!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Chat Lockdown", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

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

        await message.reply_text(
            f"Chat has been locked down by {message.from_user.mention if message.from_user else 'Anonymous'}."
        )
    
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )
