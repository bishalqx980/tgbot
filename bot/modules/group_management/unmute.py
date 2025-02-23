from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_message(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)
    if not _chk_per:
        return
    
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.reply_message(update, "I'm not an admin in this chat!")
        return
    
    if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_message(update, "You aren't an admin in this chat!")
        return
    
    if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
        if not _chk_per["user_permission"].can_restrict_members:
            await Message.reply_message(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not _chk_per["bot_permission"].can_restrict_members:
        await Message.reply_message(update, "I don't have enough rights to restrict/unrestrict chat member!")
        return
    
    if not reply:
        await Message.reply_message(update, "I don't know who you are talking about! Reply the member whom you want to unmute!\nTo mention with reason eg. <code>/unmute reason</code>")
        return
    
    if _chk_per["victim_permission"].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _chk_per["_bot_info"]["id"] == victim.id:
            await Message.reply_message(update, "Are you out of mind?")
        else:
            await Message.reply_message(update, f"Chat admin's can't be muted or unmuted!")
        return
    
    if _chk_per["victim_permission"].status != ChatMember.RESTRICTED:
        await Message.reply_message(update, "The user isn't muted, so how could I unmute?")
        return
    
    permissions = {
        "can_send_other_messages": True,
        "can_invite_users": True,
        "can_send_polls": True,
        "can_send_messages": True,
        "can_change_info": True,
        "can_pin_messages": True,
        "can_add_web_page_previews": True,
        "can_manage_topics": True,
        "can_send_audios": True,
        "can_send_documents": True,
        "can_send_photos": True,
        "can_send_videos": True,
        "can_send_video_notes": True,
        "can_send_voice_notes": True
    }

    try:
        await bot.restrict_chat_member(chat.id, victim.id, permissions)
    except Exception as e:
        logger.error(e)
        await Message.reply_message(update, str(e))
        return
    
    if not is_silent:
        msg = f"{victim.mention_html()} has been unmuted in this chat!\n<b>Admin:</b> {user.first_name}"
        if reason:
            msg = f"{msg}\n<b>Reason</b>: {reason}"
        
        await Message.reply_message(update, msg)


async def func_sunmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_unmute(update, context, is_silent=True)
