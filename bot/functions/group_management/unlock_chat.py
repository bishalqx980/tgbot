from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import bot, logger
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.functions.group_management.pm_error import _pm_error
from bot.functions.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.functions.group_management.check_permission import _check_permission


async def func_unlockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
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
        if not _chk_per["user_permission"].can_change_info:
            await Message.edit_message(update, "You don't have enough rights to manage this chat!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_change_info:
        await Message.edit_message(update, "I don't have enough rights to manage this chat!", sent_msg)
        return
    
    permissions = {
        "can_send_messages": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_send_audios": True,
        "can_send_documents": True,
        "can_send_photos": True,
        "can_send_videos": True,
        "can_send_video_notes": True,
        "can_send_voice_notes": True,
        "can_send_polls": True
    }

    try:
        await bot.set_chat_permissions(chat.id, permissions)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return

    await Message.edit_message(update, f"This chat has been unlocked!\n<b>Admin:</b> {user.first_name}", sent_msg)
    await _log_channel(update, chat, user, action="CHAT_UNLOCK")
