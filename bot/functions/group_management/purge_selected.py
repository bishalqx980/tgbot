from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins
from bot.modules.database import MemoryDB

async def func_purgefrom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    if not re_msg:
        await effective_message.reply_text(
            "Reply the message where you want to purge from! Then use /purgeto to start.\n"
            "Note: All messages between purgefrom and purgeto will be deleted!"
        )
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_delete_messages:
        await effective_message.reply_text("You don't have enough permission to delete chat messages!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins["is_bot_admin"].can_delete_messages:
        await effective_message.reply_text("I don't have enough permission to delete chat messages!")
        return
    
    await effective_message.delete()
    sent_message = await effective_message.reply_text("Now reply the last message to delete by /purgeto command.")
    
    data = {
        "purge_user_id": user.id,
        "purge_message_id": re_msg.id,
        "sent_message_id": sent_message.id
    }

    MemoryDB.insert("data_center", chat.id, data)


async def func_purgeto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if not re_msg:
        await effective_message.reply_text(
            "Reply the last message to delete.\n"
            "Note: All messages between purgefrom and purgeto will be deleted!"
        )
        return
    
    data_center = MemoryDB.data_center.get(chat.id)
    if not data_center:
        await effective_message.reply_text("Use /purgefrom for details.")
        return
    
    purge_user_id = data_center.get("purge_user_id") # for checking is that same user
    purge_message_id = data_center.get("purge_message_id")
    sent_message_id = data_center.get("sent_message_id") # for deleting this message

    if not purge_message_id:
        await effective_message.reply_text("Use /purgefrom for details.")
        return
    
    if purge_user_id != user.id:
        await effective_message.reply_text("Task isn't yours!")
        return
    
    message_ids = []
    for message_id in range(purge_message_id, re_msg.id):
        message_ids.append(message_id)
    
    message_ids.append(sent_message_id)

    try:
        await chat.delete_messages(message_ids)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    # cleaning memory
    data = {
        "purge_user_id": None,
        "purge_message_id": None,
        "sent_message_id": None
    }

    MemoryDB.insert("data_center", chat.id, data)
    
    await effective_message.reply_text("Purge completed!")
    await effective_message.delete()
