from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ... import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_unpinall(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_pin_messages:
        await effective_message.reply_text("You don't have enough permission to unpin messages!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins["is_bot_admin"].can_pin_messages:
        await effective_message.reply_text("I don't have enough permission to unpin messages!")
        return
    
    try:
        await chat.unpin_all_messages()
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        await effective_message.reply_text("Chat's all pinned messages has been unpinned!")


async def func_sunpinall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()
    await func_unpinall(update, context, is_silent=True)
