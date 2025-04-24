from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.chat_admins import ChatAdmins

async def func_unpin(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
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
        await effective_message.reply_text("I don't know which message to unpin! Reply the message to unpin!")
        return
    
    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins.is_user_admin and not chat_admins.is_user_admin.can_pin_messages:
        await effective_message.reply_text("You don't have enough permission to unpin messages!")
        return
    
    if not chat_admins.is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins.is_bot_admin.can_pin_messages:
        await effective_message.reply_text("I don't have enough permission to unpin messages!")
        return
    
    try:
        await chat.unpin_message(re_msg.id)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        await effective_message.reply_text(f"<a href='{re_msg.link}'>Message</a> has been unpinned!")


async def func_sunpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()
    await func_unpin(update, context, is_silent=True)
