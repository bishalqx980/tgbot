from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger


from bot.functions.group_management.pm_error import _pm_error

from bot.functions.group_management.check_permission import _check_permission


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return

    

    if user.is_bot:
        await effective_message.reply_text("I don't take permission from anonymous admins!")
        return
    
    sent_message = await effective_message.reply_text("💭")
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
        await Message.edit_message(update, "I don't know who you are talking about! Reply the member whom you want to unban!\nTo mention with reason eg. <code>/unban reason</code>", sent_msg)
        return
    
    if _chk_per["victim_permission"].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if bot.id == victim.id:
            await Message.edit_message(update, "Are you out of mind?", sent_msg)
        else:
            await Message.edit_message(update, f"Chat admin's can't be banned or unbanned.", sent_msg)
        return
    
    if _chk_per["victim_permission"].status != ChatMember.BANNED:
        await Message.edit_message(update, "The user isn't banned, so how could I unban?", sent_msg)
        return
    
    try:
        await bot.unban_chat_member(chat.id, victim.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        msg = f"{victim.mention_html()} has been unbanned in this chat!\n<b>Admin:</b> {user.first_name}"
        if reason:
            msg = f"{msg}\n<b>Reason</b>: {reason}"
        
        await Message.edit_message(update, msg, sent_msg)
    
    # Sending message to victim
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
    
    await Message.send_message(victim.id, msg)


async def func_sunban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_unban(update, context, is_silent=True)
