from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_pin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if not bot_permission.can_pin_messages:
        await Message.reply_msg(update, "I don't have enough rights to pin/unpin messages!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_pin_messages"):
            await Message.reply_msg(update, "You don't have enough rights to pin/unpin messages!")
            return
    
    if not reply:
        await Message.reply_msg(update, "Please reply the message which one you want to pin loudly!")
        return
    
    try:
        await bot.pin_chat_message(chat.id, msg_id)
    except Exception as e:
        logger.error(e)
        await Message.reply_msg(update, e)
        return

    await Message.reply_msg(update, f"Message pinned & notified everyone!")
    await _log_channel(update, chat, user, action="PIN")
