from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission
from bot.modules.group_management.extract_time_reason import _extract_time_reason


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    inline_text = " ".join(context.args)
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, victim_permission = _chk_per
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
        
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not user_permission.can_restrict_members:
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not bot_permission.can_restrict_members:
        await Message.reply_msg(update, "I don't have enough rights to restrict/unrestrict chat member!")
        return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to mute!\nTo mention with reason eg. <code>/mute reason</code>\nTo give a duration of mute <code>/mute time</code> or <code>/mute time reason</code>\n<pre>50second » 50s\n45minute » 45m\n5hour » 5h\n3days » 3d</pre>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _bot_info.get("id") == victim.id:
            await Message.reply_msg(update, "I'm not going to mute myself!")
            return
        # Super power for chat owner
        elif victim_permission.status == ChatMember.ADMINISTRATOR and user_permission.status == ChatMember.OWNER:
            pass
        else:
            await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking!")
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
        error_msg = await Message.reply_msg(update, e)
        if not error_msg:
            await Message.reply_msg(update, e.message)
        return
    
    if not is_silent:
        msg = f"Shh... {victim.mention_html()} has been muted in this chat!\n<b>Admin:</b> {user.first_name}\n"
        
        if logical_time:
            msg = f"{msg}<b>Duration</b>: {logical_time}\n"

        if reason:
            msg = f"{msg}<b>Reason</b>: {reason}"
        
        await Message.reply_msg(update, msg)


async def func_smute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.del_msg(chat.id, e_msg)
    await func_mute(update, context, is_silent=True)
