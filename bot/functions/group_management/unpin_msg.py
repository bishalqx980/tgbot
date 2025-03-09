from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import bot, logger
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.functions.group_management.pm_error import _pm_error
from bot.functions.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.functions.group_management.check_permission import _check_permission


async def func_unpin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None
    
    if chat.type == ChatType.PRIVATE:
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
        if not _chk_per["user_permission"].can_pin_messages:
            await Message.edit_message(update, "You don't have enough rights to pin/unpin messages!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_pin_messages:
        await Message.edit_message(update, "I don't have enough rights to pin/unpin messages!", sent_msg)
        return

    if not reply:
        await Message.edit_message(update, "This command will unpin replied message (which is already pinned)!", sent_msg)
        return
    
    try:
        await bot.unpin_chat_message(chat.id, msg_id)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        await Message.edit_message(update, f"Message unpinned!", sent_msg)
    await _log_channel(update, chat, user, action="UNPIN")


async def func_sunpin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_unpin_msg(update, context, is_silent=True)
