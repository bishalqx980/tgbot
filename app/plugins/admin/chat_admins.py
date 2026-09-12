from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus

from app import bot, COMMAND_PREFIXES
from app.decorators import sudo_required, privatechat_only
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "chatadmins",
    "commands": ["chatadmins", "cadmins"], # list of commands including aliases

    "description": "Get specified chat admin list! E.g. `/chatadmins CHAT_ID or USERNAME`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Chat Admins", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@sudo_required
async def func_(_, message: Message):
    chat_id = CommandArgs(message.text, message.command) # CHAT_ID or USERNAME

    if not chat_id:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )

    # int convert to fix contacts.ResolvePhone error
    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        pass
    
    sent_message = await message.reply("Please wait...")
    
    chat_owner = "**Owner:**\n"
    chat_admins = ""
    
    try:

        async for admin in bot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            # Anonymous admins will be listed too
            textline = f"• {admin.user.mention} - <i>{admin.custom_title or ''}</i>\n"

            if admin.status in [ChatMemberStatus.OWNER]:
                chat_owner += textline
            
            elif not admin.user.is_bot:
                chat_admins += textline
    
    except Exception as e:
        return await sent_message.edit_text(f"Error: {e}")
    
    if chat_admins: chat_admins = f"\n**Admin's:**\n{chat_admins}"

    await sent_message.edit_text(
        f"> Admins of `{chat_id}`\n\n"
        f"{chat_owner}{chat_admins}"
    )
