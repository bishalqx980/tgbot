from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from bot.utils.database import MemoryDB, MongoDB, database_search
from bot.handlers.group.auxiliary.chat_admins import ChatAdmins

async def query_groupManagement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("admin_")

    if query_data == "none":
        await query.answer()
        return
    
    elif query_data == "anonymous_verify":
        await query.answer("Verified!")
        MemoryDB.insert("data_center", chat.id, {"anonymous_admin": user})
        return
    
    elif query_data.startswith("remove_warn"):
        # expecting remove_warn_[victim_id]
        victim_id = query_data.removeprefix("remove_warn_")

        chat_admins = ChatAdmins()
        await chat_admins.fetch_admins(chat, user_id=user.id)
        
        if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
            await query.answer("You aren't an admin in this chat!", True)
            return
        
        chat_data = database_search("chats_data", "chat_id", chat.id)
        if not chat_data:
            await query.answer("Chat isn't registered! Remove/Block me from this chat then add me again!", True)
            return
        
        warns = chat_data.get("warns") or {}
        victim_warns = warns.get(str(victim_id)) or {} # mongodb doesn't allow int doc key
        victim_mention = victim_warns.get("victim_mention")
        victim_warns.clear()
        
        response = MongoDB.update("chats_data", "chat_id", chat.id, "warns", warns)
        if response:
            MemoryDB.insert("chats_data", chat.id, {"warns": warns})
        
        try:
            await chat.restrict_member(int(victim_id), ChatPermissions.all_permissions())
        except Exception as e:
            await query.edit_message_text(str(e))
            return
        
        await query.edit_message_text(f"Great! Admin {user.mention_html()} has cleared all warnings of {victim_mention or f'<code>{victim_id}</code>'}.")
