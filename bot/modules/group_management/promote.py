from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    admin_title = " ".join(context.args)
    
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
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if not bot_permission.can_promote_members:
        await Message.reply_msg(update, "I don't have enough rights to promote/demote chat member!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_promote_members"):
            await Message.reply_msg(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to promote!\nTo set admin_title eg. <code>/promote admin_title</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        if _bot_info.id == victim.id:
            await Message.reply_msg(update, "I'm already an admin!")
        else:
            await Message.reply_msg(update, "The user is already an admin!")
        return
    
    try:
        await bot.promote_chat_member(chat.id, victim.id, can_manage_video_chats=True)
    except Exception as e:
        logger.error(e)
        await Message.reply_msg(update, e)
        return

    msg = f"{victim.mention_html()} has been promoted!\n<b>Admin</b>: {user.first_name}"
    if admin_title:
        try:
            await bot.set_chat_administrator_custom_title(chat.id, victim.id, admin_title)
            msg = f"{msg}\nAdmin title: {admin_title}"
        except Exception as e:
            logger.error(e)
            await Message.reply_msg(update, e)
    
    await Message.reply_msg(update, msg)
    await _log_channel(update, chat, user, victim, action="PROMOTE")
