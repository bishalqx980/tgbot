from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_invite,
    user_admin,
    user_can_invite
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "invite",
    "commands": ["invite"], # list of commands including aliases

    "description": "Generate invite link for group chat!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Invite", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_invite
@bot_admin
@bot_can_invite
async def func_(_, message: Message):
    # public chat link
    public_link = message.chat.invite_link

    if public_link:
        return await message.reply_text(
            f"> {message.chat.title}\n\n"
            f"Invite link : {public_link}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Open link", url=public_link),
                InlineKeyboardButton("Copy link", copy_text=public_link)
            ]])
        )
    
    try:
        
        invite_link_data = await bot.create_chat_invite_link(
            chat_id=message.chat.id,
            name=message.from_user.first_name if message.from_user else "Anonymous"
        )

        link = invite_link_data.invite_link
        expire_date = invite_link_data.expire_date.strftime("%Y-%m-%d %H:%M:%S") if invite_link_data.expire_date else '♾️'

        await message.reply_text(
            (
                f"> {message.chat.title}\n\n"
                f"• Invite link : {link}\n"
                f"• Expire date : {expire_date}\n"
                f"• Member limit : {invite_link_data.member_limit or '♾️'}\n"
                f"• Creation time : {invite_link_data.date.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"• Creator : {invite_link_data.name}"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Open link", url=link),
                InlineKeyboardButton("Copy link", copy_text=link)
            ]])
        )

    except Exception as e:
        return await message.reply_text(f"Error: {e}")
