from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.check_del_cmd import _check_del_cmd
from bot.modules.group_management.check_permission import _check_permission


async def func_demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

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
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if not bot_permission.can_promote_members:
        await Message.reply_msg(update, "I don't have enough rights to promote/demote chat member!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_promote_members"):
            await Message.reply_msg(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to demote!")
        return
    
    try:
        await bot.promote_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"{user.mention_html()} has demoted user {victim.mention_html()} in this chat!")
        await _log_channel(context, chat, user, victim, action="DEMOTE")
    except Exception as e:
        logger.error(e)
        await Message.send_msg(chat.id, f"Error: {e}")
