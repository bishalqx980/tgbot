from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger


from bot.functions.group_management.pm_error import _pm_error
from bot.functions.group_management.log_channel import _log_channel

from bot.functions.group_management.check_permission import _check_permission


async def func_unpinall_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    
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
    
    if _chk_per["user_permission"].status != ChatMember.OWNER:
        await Message.edit_message(update, "This command is only for group owner!", sent_msg)
        return
    
    if not _chk_per["bot_permission"].can_pin_messages:
        await Message.edit_message(update, "I don't have enough rights to pin/unpin messages!", sent_msg)
        return
    
    try:
        await bot.unpin_all_chat_messages(chat.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        await Message.edit_message(update, f"All message unpinned!", sent_msg)
    await _log_channel(update, chat, user, action="UNPIN_ALL_MSG")


async def func_sunpinall_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_unpinall_msg(update, context, is_silent=True)
