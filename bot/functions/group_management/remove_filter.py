from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger


from bot.modules.database import MemoryDB, MongoDB
from bot.modules.database.common import database_search
from bot.functions.group_management.pm_error import _pm_error

from bot.functions.group_management.check_permission import _check_permission


async def func_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    keyword = " ".join(context.args).lower()
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    

    if user.is_bot:
        await effective_message.reply_text("I don't take permission from anonymous admins!")
        return
    
    sent_msg = await effective_message.reply_text("💭")
    _chk_per = await _check_permission(update, user=user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Something went wrong!", sent_msg)
        return
        
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.edit_message(update, "You aren't an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
        if not _chk_per["user_permission"].can_change_info:
            await Message.edit_message(update, "You don't have enough rights to manage this chat!", sent_msg)
            return
    
    if not keyword:
        msg = (
            "To remove a existing filter use <code>/remove keyword</code>\n"
            "Use <code>clear_all</code> instead of keyword, to delete all filters of this chat!"
        )
        await Message.edit_message(update, msg, sent_msg)
        return

    response, database_data = database_search("groups", "chat_id", chat.id)
    if database[0] == False:
        await Message.edit_message(update, database[1], sent_msg)
        return
    
    find_group = database[1]
    
    filters = find_group.get("filters")

    if filters and keyword:
        if keyword == "clear_all":
            MongoDB.update_db("groups", "chat_id", chat.id, "filters", None)
            await Message.edit_message(update, f"All filters of this chat has been removed!\n<b>Admin:</b> {user.first_name}", sent_msg)

            group_data = MongoDB.find_one("groups", "chat_id", chat.id)
            MemoryDB.insert_data("chat_data", chat.id, group_data)
            return
        
        try:
            if keyword.lower() in filters:
                del filters[keyword]
                MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
                await Message.edit_message(update, f"<code>{keyword}</code> filter has been removed!\n<b>Admin:</b> {user.first_name}", sent_msg)
            else:
                await Message.edit_message(update, "There are no such filter available for this chat to delete!\nCheckout /filters", sent_msg)
                return
            
            group_data = MongoDB.find_one("groups", "chat_id", chat.id)
            MemoryDB.insert_data("chat_data", chat.id, group_data)
        except Exception as e:
            logger.error(e)
            await Message.edit_message(update, str(e), sent_msg)
