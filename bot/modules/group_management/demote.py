from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_demote(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

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
    
    _bot_info, bot_permission, user_permission, victim_permission = _chk_per
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_message(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_message(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not user_permission.can_promote_members:
            await Message.reply_message(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not bot_permission.can_promote_members:
        await Message.reply_message(update, "I don't have enough rights to promote/demote chat member!")
        return
    
    if not reply:
        await Message.reply_message(update, "I don't know who you are talking about! Reply the member whom you want to demote!")
        return
    
    if victim_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_message(update, "The user isn't an admin!")
        return
    
    if _bot_info.get("id") == victim.id:
        await Message.reply_message(update, "I'm not going to do this!")
        return
    
    try:
        await bot.promote_chat_member(chat.id, victim.id)
    except Exception as e:
        logger.error(e)
        await Message.reply_message(update, str(e))
        return
    
    if not is_silent:
        await Message.reply_message(update, f"{victim.mention_html()} has been demoted!\n<b>Admin:</b> {user.first_name}")


async def func_sdemote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_demote(update, context, is_silent=True)
