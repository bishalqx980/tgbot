from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
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
    
    sent_msg = await Message.reply_message(update, "💭")
    _chk_per = await _check_permission(update, victim, user)
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
        if not _chk_per["user_permission"].can_restrict_members:
            await Message.edit_message(update, "You don't have enough rights to restrict/unrestrict chat member!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_restrict_members:
        await Message.edit_message(update, "I don't have enough rights to restrict/unrestrict chat member!", sent_msg)
        return
    
    if not reply:
        await Message.edit_message(update, "I don't know who you are talking about! Reply the member whom you want to ban!\nTo mention with reason eg. <code>/ban reason</code>", sent_msg)
        return
    
    if _chk_per["victim_permission"].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if bot.id == victim.id:
            await Message.edit_message(update, "I'm not going to ban myself!", sent_msg)
            return
        # Super power for chat owner
        elif _chk_per["victim_permission"].status == ChatMember.ADMINISTRATOR and _chk_per["user_permission"].status == ChatMember.OWNER:
            pass
        else:
            await Message.edit_message(update, "I'm not going to ban an admin! You must be joking!", sent_msg)
            return
    
    if _chk_per["victim_permission"].status == ChatMember.BANNED:
        await Message.edit_message(update, "The user is already banned in this chat!", sent_msg)
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        msg = f"{victim.mention_html()} has been banned in this chat!\n<b>Admin:</b> {user.first_name}"
        if reason:
            msg = f"{msg}\n<b>Reason</b>: {reason}"
        
        await Message.edit_message(update, msg, sent_msg)

    # send message to banned user private chat
    msg = f"{user.mention_html()} has banned you in {chat.title}!"
    if reason:
        msg = f"{msg}\n<b>Reason</b>: {reason}"
    
    await Message.send_message(victim.id, msg)


async def func_sban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_ban(update, context, is_silent=True)
