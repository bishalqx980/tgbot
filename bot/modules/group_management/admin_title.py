from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_admintitle(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=bool(None)):
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
    
    _bot_info, bot_permission, user_permission, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not user_permission.can_promote_members:
            await Message.reply_msg(update, "You don't have enough rights to set admin title!")
            return
    
    if not bot_permission.can_promote_members:
        await Message.reply_msg(update, "I don't have enough rights to set admin title!")
        return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the admin to set admin title!\neg. <code>/admintitle admin_title</code>\n<i>Note:</i> bot can only set admin title if that admin is promoted by bot!")
        return
    
    if not admin_title:
        await Message.reply_msg(update, "Use <code>/admintitle admin_title</code>\n<i>Note:</i> bot can only set admin title if that admin is promoted by bot!")
        return
    
    try:
        await bot.set_chat_administrator_custom_title(chat.id, victim.id, admin_title)
        msg = (
            f"{victim.mention_html()}'s admin title has been updated!\n"
            f"<b>Admin:</b> {user.first_name}\n"
            f"<b>New admin title:</b> {admin_title}"
        )

        if not is_silent:
            await Message.reply_msg(update, msg)
        
        await _log_channel(update, chat, user, victim, action=f"ADMIN_TITLE ({admin_title})")
    except Exception as e:
        logger.error(e)
        error_msg = await Message.reply_msg(update, e)
        if not error_msg:
            await Message.reply_msg(update, e.message) 


async def func_sadmintitle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.del_msg(chat.id, e_msg)
    await func_admintitle(update, context, is_silent=True)
