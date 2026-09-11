from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus

from app import bot, COMMAND_PREFIXES
from app.decorators import groupchat_only


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "adminlist",
    "commands": ["admins", "adminlist"], # list of commands including aliases

    "description": "Get chat admins list.",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Admins", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
async def func_(_, message: Message):
    owner = "**Owner:**\n"
    admins = []

    async for admin in message.chat.get_members(
        filter=ChatMembersFilter.ADMINISTRATORS
    ):
        custom_title = f"- <i>{admin.custom_title}</i>" if admin.custom_title else ""
        admin_name = "Anonymous" if admin.privileges.is_anonymous else admin.user.mention

        line = f"• {admin_name} {custom_title}"

        if admin.status == ChatMemberStatus.OWNER:
            owner += line

        elif not admin.user.is_bot:
            admins.append(line)
        
    if admins:
        admins = f"**Admin's:**\n{'\n'.join(admins)}"

    await message.reply_text(
        f"> {message.chat.title}\n\n"
        f"{owner}\n\n"
        f"{admins or ''}"
    )
