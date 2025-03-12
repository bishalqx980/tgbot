from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger


from bot.functions.group_management.pm_error import _pm_error

from bot.functions.group_management.check_permission import _check_permission
from bot.functions.group_management.extract_time_reason import _extract_time_reason


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    inline_text = " ".join(context.args)
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    

    if user.is_bot:
        await effective_message.reply_text("I don't take permission from anonymous admins!")
        return
    
    sent_msg = await effective_message.reply_text("💭")
    _chk_per = await _check_permission(update, victim, user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Something went wrong!", sent_msg)
        return
    
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
        return
        
    if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.edit_message(update, "You aren't an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
        if not _chk_per["user_permission"].can_restrict_members:
            await Message.edit_message(update, "You don't have enough rights to restrict/unrestrict chat member!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_restrict_members:
        await Message.edit_message(update, "I don't have enough rights to restrict/unrestrict chat member!", sent_msg)
        return
    
    if not reply:
        await Message.edit_message(update, "I don't know who you are talking about! Reply the member whom you want to mute!\nTo mention with reason eg. <code>/mute reason</code>\nTo give a duration of mute <code>/mute time</code> or <code>/mute time reason</code>\n<blockquote>Time should be like this\n50second » 50s\n45minute » 45m\n5hour » 5h\n3days » 3d\n[s, m, h, d]</blockquote>", sent_msg)
        return
    
    if _chk_per["victim_permission"].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if bot.id == victim.id:
            await Message.edit_message(update, "I'm not going to mute myself!", sent_msg)
            return
        # Super power for chat owner
        elif _chk_per["victim_permission"].status == ChatMember.ADMINISTRATOR and _chk_per["user_permission"].status == ChatMember.OWNER:
            pass
        else:
            await Message.edit_message(update, f"I'm not going to mute an admin! You must be joking!", sent_msg)
            return
    
    permissions = {
        "can_send_other_messages": False,
        "can_invite_users": False,
        "can_send_polls": False,
        "can_send_messages": False,
        "can_change_info": False,
        "can_pin_messages": False,
        "can_add_web_page_previews": False,
        "can_manage_topics": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_send_video_notes": False,
        "can_send_voice_notes": False
    }

    until_date = logical_time = reason = None

    if inline_text:
        time, logical_time, reason = await _extract_time_reason(reason)
        if time:
            until_date = time
    
    try:
        await bot.restrict_chat_member(chat.id, victim.id, permissions, until_date)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        msg = f"Shh... {victim.mention_html()} has been muted in this chat!\n<b>Admin:</b> {user.first_name}\n"
        
        if logical_time:
            msg = f"{msg}<b>Duration</b>: {logical_time}\n"

        if reason:
            msg = f"{msg}<b>Reason</b>: {reason}"
        
        await Message.edit_message(update, msg, sent_msg)


async def func_smute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_mute(update, context, is_silent=True)
