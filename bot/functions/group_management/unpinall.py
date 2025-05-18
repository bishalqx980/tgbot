from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.chat_admins import ChatAdmins

async def func_unpinall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    cmd_prefix = effective_message.text[1]
    is_silent = False
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if cmd_prefix == "s":
        is_silent = True
        try:
            await effective_message.delete()
        except:
            pass
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
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
        await chat.unpin_all_messages()
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        await effective_message.reply_text("Chat's all pinned messages has been unpinned!")
