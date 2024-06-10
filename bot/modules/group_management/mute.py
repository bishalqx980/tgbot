from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.check_del_cmd import _check_del_cmd
from bot.modules.group_management.check_permission import _check_permission
from bot.modules.group_management.extract_time_reason import _extract_time_reason


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if not bot_permission.can_restrict_members:
        await Message.reply_msg(update, "I don't have enough rights to restrict/unrestrict chat member!")
        return
        
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to mute!\nTo mention with reason eg. <code>/mute reason</code>\nTo give a duration of mute <code>/mute time</code> or <code>/mute time reason</code>\n<pre>50second » 50s\n45minute » 45m\n5hour » 5h\n3days » 3d</pre>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _bot_info.id == victim.id:
            await Message.reply_msg(update, "I'm not going to mute myself!")
        else:
            await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking!")
        return
    
    if victim_permission.status == ChatMember.RESTRICTED:
        await Message.reply_msg(update, "The user is already muted in this chat!")
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

    msg = f"Shh... {victim.mention_html()} has been muted in this chat!\n<b>Admin</b>: {user.first_name}\n"
    until_date = None
    time = None

    if reason:
        time, logical_time, reason = await _extract_time_reason(reason)
        if time:
            msg = f"{msg}<b>Duration</b>: {logical_time}\n"
            until_date = time
        if reason:
            msg = f"{msg}<b>Reason</b>: {reason}"
    
    try:
        await bot.restrict_chat_member(chat.id, victim.id, permissions, until_date)
        await Message.reply_msg(update, msg)
    except Exception as e:
        logger.error(e)
        await Message.send_msg(chat.id, f"Error: {e}")
