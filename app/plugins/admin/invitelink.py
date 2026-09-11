from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, admin_require
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "invitelink",
    "commands": ["invitelink", "il"], # list of commands including aliases

    "description": "Get invite link of specified chat! E.g. `/invitelink CHAT_ID`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Invite Link", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@admin_require
async def func_(_, message: Message):
    # this is the CHATID
    chat_id = CommandArgs(message.text, message.command)

    if not chat_id:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    sent_message = await message.reply("Please wait...")

    # int convert to fix contacts.ResolvePhone error
    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        pass

    try:
        invite_data = await bot.create_chat_invite_link(
            chat_id,
            expire_date=datetime.now() + timedelta(days=1), # expire after 1 day of creation
            member_limit=1
        )
    except Exception as e:
        return await sent_message.edit_text(f"Error: {e}")
    
    await sent_message.edit_text(
        "> Invite link generated successfully!\n"
        f"**Creator:** <i>{invite_data.creator.first_name if invite_data.creator else ''}</i>\n"
        f"**Member Limit:** <i>{invite_data.member_limit}</i>\n"
        f"**Expire Date:** <i>{invite_data.expire_date}</i>",

        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Join",
                url=invite_data.invite_link
            ),
            InlineKeyboardButton(
                "Copy Link",
                copy_text=invite_data.invite_link
            )
        ]])
    )
