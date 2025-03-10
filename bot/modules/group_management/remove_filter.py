from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    keyword = " ".join(context.args).lower()
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_message(update, "I don't take permission from anonymous admins!")
        return
    
    sent_msg = await Message.reply_message(update, "💭")
    _chk_per = await _check_permission(update, user=user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
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

    db = await global_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.edit_message(update, db[1], sent_msg)
        return
    
    find_group = db[1]
    
    filters = find_group.get("filters")

    if filters and keyword:
        if keyword == "clear_all":
            await MongoDB.update_db("groups", "chat_id", chat.id, "filters", None)
            await Message.edit_message(update, f"All filters of this chat has been removed!\n<b>Admin:</b> {user.first_name}", sent_msg)

            group_data = await MongoDB.find_one("groups", "chat_id", chat.id)
            await LOCAL_DATABASE.insert_data("groups", chat.id, group_data)
            return
        
        try:
            if keyword.lower() in filters:
                del filters[keyword]
                await MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
                await Message.edit_message(update, f"<code>{keyword}</code> filter has been removed!\n<b>Admin:</b> {user.first_name}", sent_msg)
            else:
                await Message.edit_message(update, "There are no such filter available for this chat to delete!\nCheckout /filters", sent_msg)
                return
            
            group_data = await MongoDB.find_one("groups", "chat_id", chat.id)
            await LOCAL_DATABASE.insert_data("groups", chat.id, group_data)
        except Exception as e:
            logger.error(e)
            await Message.edit_message(update, str(e), sent_msg)
