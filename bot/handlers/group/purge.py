from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.decorators.pm_error import pm_error
from .auxiliary.chat_admins import ChatAdmins
from .auxiliary.anonymous_admin import anonymousAdmin

@pm_error
async def func_purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message

    cmd_prefix = effective_message.text[1]
    is_silent = False
    
    if cmd_prefix == "s":
        is_silent = True
        try:
            await effective_message.delete()
        except:
            pass
    
    if user.is_bot:
        user = await anonymousAdmin(chat, effective_message)
        if not user:
            return
    
    if not re_msg:
        await effective_message.reply_text("Reply the message where you want to purge from!")
        return
    
    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins.is_user_admin and not chat_admins.is_user_admin.can_delete_messages:
        await effective_message.reply_text("You don't have enough permission to delete chat messages!")
        return
    
    if not chat_admins.is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins.is_bot_admin.can_delete_messages:
        await effective_message.reply_text("I don't have enough permission to delete chat messages!")
        return
    
    sent_message = await effective_message.reply_text("Purge started!")
    
    message_ids = []
    for message_id in range(re_msg.id, effective_message.id + 1):
        message_ids.append(message_id)
    
    try:
        await chat.delete_messages(message_ids)
    except Exception as e:
        await sent_message.edit_text(str(e))
        return
    
    if is_silent:
        await sent_message.delete()
    else:
        await sent_message.edit_text("Purge completed!")
