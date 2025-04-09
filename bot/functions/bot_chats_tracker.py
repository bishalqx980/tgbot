from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ..modules.database import MemoryDB, MongoDB

async def bot_chats_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    **Tracks Groups/Private chat (where bot is added/removed/promoted/demoted)**
    """
    chat = update.effective_chat
    chat_update = update.my_chat_member

    user = chat_update.from_user
    old_status = chat_update.old_chat_member.status
    new_status = chat_update.new_chat_member.status
    text = None

    if chat.type == ChatType.PRIVATE:
        # checking database entry
        user_data = MongoDB.find_one("users", "user_id", user.id)
        if not user_data:
            data = {
                "user_id": user.id,
                "name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code
            }

            MongoDB.insert("users", data)
            MemoryDB.insert("user_data", user.id, data)
        
        # checking member status & updating database
        active_status = new_status == ChatMember.MEMBER
        MongoDB.update("users", "user_id", user.id, "active_status", active_status)
    
    elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        # checking database entry
        chat_data = MongoDB.find_one("groups", "chat_id", chat.id)
        if not chat_data:
            data = {
                "chat_id": chat.id,
                "title": chat.title
            }

            MongoDB.insert("groups", data)
            MemoryDB.insert("chat_data", chat.id, data)
        
        if old_status in [ChatMember.LEFT, ChatMember.BANNED] and new_status == ChatMember.MEMBER:
            text = (
                "Thanks for adding me in this nice chat!\n"
                "Please make me admin in chat, so I can help you managing this chat effectively!\n"
                "/help for bot help..."
            )
        
        # promotion
        elif old_status != ChatMember.ADMINISTRATOR and new_status == ChatMember.ADMINISTRATOR:
            text = (
                "Thanks for adding me as an admin!\n"
                "Don't forget to checkout /help section..."
            )
        
        # demotion
        elif old_status == ChatMember.ADMINISTRATOR and new_status == ChatMember.MEMBER:
            text = (
                "Ohh dear, have I done something wrong!\n"
                "I wish I could help..."
            )
        
        if text:
            await context.bot.send_message(chat.id, text)
    
    elif chat.type == ChatType.CHANNEL and new_status == ChatMember.ADMINISTRATOR:
        await context.bot.send_message(user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
