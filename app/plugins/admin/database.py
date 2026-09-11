import json
from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.database import MongoDB
from app.decorators import admin_require, privatechat_only
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "database",
    "commands": ["database", "db"], # list of commands including aliases

    "description": "Get database info or specific chat info stored on database! E.g. `/database CHAT_ID`",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Database", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@admin_require
async def func_(_, message: Message):
    # CHAT ID or USER ID // Not username
    victim_id = CommandArgs(message.text, message.command)

    sent_message = await message.reply("Fetching database...")

    if not victim_id:
        database_info = MongoDB.database_info()
        msg_storage = "> **Database information**\n\n"

        for info in database_info:
            info = database_info[info]
            msg_storage += (
                f"**• Document:** <i>{info.get('name')}</i>\n"
                f"**• Quantity:** `{info.get('quantity')}`\n"
                f"**• Size:** `{info.get('size')}`\n"
                f"**• A. size:** `{info.get('acsize')}`\n\n"
            )
        
        active_status = MongoDB.get_field_values(MongoDB.USERS, "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)
        
        return await sent_message.edit_text(
            f"{msg_storage}" # already has 2 escapes
            f"**• Active users:** `{active_users}`\n"
            f"**• Inactive users:** `{inactive_users}`\n\n"
            f"> **Note:** `/{message.command[0]} CHAT_ID` to get specific chat database information."
        )

    # int convert to fix contacts.ResolvePhone error
    try:
        victim_id = int(victim_id)
    except (ValueError, TypeError) as e:
        return await sent_message.edit_text(f"Error: Invalid CHAT_ID! {e}")
    
    # if chat_id given
    if "-100" in str(victim_id):
        chat_data = MongoDB.search(MongoDB.CHATS, "chat_id", victim_id) # victim_id as int
        if not chat_data:
            return await sent_message.edit_text("Error: Chat wasn't found!")
        
        try:
            chat_info = await bot.get_chat(victim_id) # as int
        except:
            chat_info = None
            btn = None
        
        chat_title = chat_info.title if chat_info else chat_data.get('title')
        chat_invite_link = chat_info.invite_link if chat_info else None

        text = (
            "> **Database information**\n\n"

            f"• Title: {chat_title}\n"
            f"• ID: `{victim_id}`\n\n"

            f"• Language: `{chat_data.get('lang')}`\n"
            f"• Auto translate: `{chat_data.get('auto_tr') or False}`\n"
            f"• Echo: `{chat_data.get('echo') or False}`\n"
            f"• Antibot: `{chat_data.get('antibot') or False}`\n"
            f"• Welcome Members: `{chat_data.get('welcome_user') or False}`\n"
            f"• Farewell Members: `{chat_data.get('farewell_user') or False}`\n"
            f"• Join Request: `{chat_data.get('chat_join_req')}`\n"
            f"• Service Messages: `{chat_data.get('service_messages')}`\n"
            f"• Links Behave: `{chat_data.get('links_behave')}`\n"
            f"• Allowed Links: `{', '.join(chat_data.get('allowed_links') or [])}`"
        )

        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Join",
                url=chat_invite_link
            )
        ]]) if chat_invite_link else None

        custom_welcome_msg = chat_data.get('custom_welcome_msg')
        if custom_welcome_msg:
            text += (
                "\n\n> **Custom Welcome message**\n\n"
                f"> {custom_welcome_msg}"
            )
        
        chat_filters = chat_data.get('filters')
        if chat_filters:
            filters_file = BytesIO(json.dumps(chat_filters, indent=4).encode())
            filters_file.name = f"filters-{victim_id}.json"

            await message.reply_document(filters_file, caption=f"ChatID: `{victim_id}`")
    
    else:
        user_data = MongoDB.search(MongoDB.USERS, "user_id", victim_id) # victim_id as int
        if not user_data:
            return await sent_message.edit_text("Error: User wasn't found!")
        
        try:
            user_info = await bot.get_users(victim_id) # as int
        except:
            user_info = None
            btn = None
        
        user_mention = getattr(user_info, "mention", None) or user_data.get("mention")
        user_username = getattr(user_info, "username", None) or user_data.get("username")

        text = (
            "> **Database information**\n\n"

            f"• Name: {user_mention}\n"
            f"• ID: `{victim_id}`\n"
            f"• Username: @{user_username or 'username'}\n\n"

            f"• Language: `{user_data.get('lang')}`\n"
            f"• Auto translate: `{user_data.get('auto_tr') or False}`\n"
            f"• Echo: `{user_data.get('echo') or False}`\n\n"

            f"• Active status: `{user_data.get('active_status')}`"
        )

        if user_info:
            btn = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "User Profile",
                    user_id=user_info.id
                )
            ]]) if getattr(user_info, "username", None) else None
    
    # common message sender for both group chat & private chat database info
    await sent_message.edit_text(text, reply_markup=btn)
