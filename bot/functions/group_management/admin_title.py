from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.log_channel import _log_channel
from bot.functions.group_management.pm_error import _pm_error

from bot.functions.group_management.check_permission import _check_permission


async def func_admintitle(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=False):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    admin_title = " ".join(context.args)
    
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
        if not _chk_per["user_permission"].can_promote_members:
            await Message.edit_message(update, "You don't have enough rights to set admin title!", sent_msg)
            return
    
    if not _chk_per["bot_permission"].can_promote_members:
        await Message.edit_message(update, "I don't have enough rights to set admin title!", sent_msg)
        return
    
    if not reply:
        await Message.edit_message(update, "I don't know who you are talking about! Reply the admin to set admin title!\neg. <code>/admintitle admin_title</code>\n<i>Note:</i> I can only set admin title if that admin is promoted by me!", sent_msg)
        return
    
    if not admin_title:
        await Message.edit_message(update, "Use <code>/admintitle admin_title</code>\n<i>Note:</i> I can only set admin title if that admin is promoted by me!", sent_msg)
        return
    
    try:
        await bot.set_chat_administrator_custom_title(chat.id, victim.id, admin_title)
        msg = (
            f"{victim.mention_html()}'s admin title has been updated!\n"
            f"<b>Admin:</b> {user.first_name}\n"
            f"<b>New admin title:</b> {admin_title}"
        )

        if is_silent:
            await Message.delete_message(chat.id, sent_msg)
        else:
            await Message.edit_message(update, msg, sent_msg)
        
        await _log_channel(update, chat, user, victim, action=f"ADMIN_TITLE ({admin_title})")
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)


async def func_sadmintitle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_admintitle(update, context, is_silent=True)
