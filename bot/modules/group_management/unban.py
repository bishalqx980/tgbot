from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
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
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to unban!\nTo mention with reason eg. <code>/unban reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _bot_info.get("id") == victim.id:
            await Message.reply_msg(update, "Are you out of mind?")
        else:
            await Message.reply_msg(update, f"Chat admin's can't be banned or unbanned.")
        return
    
    if victim_permission.status != ChatMember.BANNED:
        await Message.reply_msg(update, "The user isn't banned, so how could I unban?")
        return
    
    try:
        await bot.unban_chat_member(chat.id, victim.id)
    except Exception as e:
        logger.error(e)
        error_msg = await Message.reply_msg(update, e)
        if not error_msg:
            await Message.reply_msg(update, e.message)
        return
    
    if not is_silent:
        msg = f"{victim.mention_html()} has been unbanned in this chat!\n<b>Admin:</b> {user.first_name}"
        if reason:
            msg = f"{msg}\n<b>Reason</b>: {reason}"
        
        await Message.reply_msg(update, msg)

    if chat.link:
        invite_link = chat.link
    else:
        try:
            create_invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            invite_link = create_invite_link.invite_link
        except Exception as e:
            logger.error(e)
            return
    
    msg = f"{user.mention_html()} has unbanned you in {chat.title}!\nYou can join again using this invite link!\nInvite Link: {invite_link}"
    if reason:
        msg = f"{msg}\n<b>Reason</b>: {reason}"
    
    await Message.send_msg(victim.id, msg)


async def func_sunban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.del_msg(chat.id, e_msg)
    await func_unban(update, context, is_silent=True)
