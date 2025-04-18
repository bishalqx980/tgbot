from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_purge(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
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
        await effective_message.reply_text("Reply the message where you want to purge from!")
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
    
    sent_message = await effective_message.reply_text("Purge started!")
    
    message_ids = []
    for message_id in range(re_msg.id, effective_message.id + 1):
        message_ids.append(message_id)
    
    try:
        await chat.delete_messages(message_ids)
    except Exception as e:
        logger.error(e)
        await context.bot.edit_message_text(str(e), chat.id, sent_message.id)
        return
    
    if is_silent:
        await context.bot.delete_message(chat.id, sent_message.id)
    
    else:
        await context.bot.edit_message_text("Purge completed!", chat.id, sent_message.id)


async def func_spurge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()
    await func_purge(update, context, is_silent=True)
