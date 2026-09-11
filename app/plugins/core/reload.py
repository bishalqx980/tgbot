from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

from app import bot, COMMAND_PREFIXES
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "reload",
    "commands": ["reload"], # list of commands including aliases

    "description": "Fix chat database! (Access Level: User)",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Reload", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    chat = message.chat
    user = message.from_user or message.sender_chat

    sent_message = await message.reply("Reloading...")

    if chat.type == ChatType.PRIVATE:
        # database entry checking if user is registered.
        user_registered = MongoDB.search(MongoDB.USERS, "user_id", user.id)

        if user_registered:
            active_status = user_registered.get("active_status")

            if not active_status:
                MongoDB.update(
                    MongoDB.USERS,
                    "user_id",
                    user.id,
                    { "active_status": True }
                )
            
            return await sent_message.edit_text(
                "Chat is already registered!"
            )

        is_ok = MongoDB.insert(
            MongoDB.USERS,
            user.id,
            {
                "user_id": user.id,
                "dc_id": user.dc_id,
                "name": user.full_name,
                "username": user.username,
                "usernames": user.usernames,
                "lang": user.language_code,
                "active_status": True
            }
        )
        
        if not is_ok:
            return await sent_message.edit_text(
                "Something went wrong! Please try again & if the problem persist then please contact our support using /support !"
            )
        
        return await sent_message.edit_text("Successfully reloaded!")
    
    else:
        # database entry checking if chat is registered.
        chat_registered = MongoDB.search(MongoDB.CHATS, "chat_id", chat.id)

        if chat_registered:
            return await sent_message.edit_text(
                "Chat is already registered!"
            )
        
        is_ok = MongoDB.insert(MongoDB.CHATS, chat.id, { "chat_id": chat.id, "title": chat.title })

        if not is_ok:
            return await sent_message.edit_text(
                "Something went wrong! Please try again & if the problem persist then please contact our support using /support !"
            )
        
        return await sent_message.edit_text("Successfully reloaded!")
