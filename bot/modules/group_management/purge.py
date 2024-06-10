from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.check_del_cmd import _check_del_cmd
from bot.modules.group_management.check_permission import _check_permission


async def func_purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await _check_del_cmd(update, context)

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
    
    if not bot_permission.can_delete_messages:
        await Message.reply_msg(update, "I don't have enough rights to delete chat messages!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_delete_messages"):
            await Message.reply_msg(update, "You don't have enough rights to delete chat messages!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know which message to delete from! Reply the message that you want to start delete from!\n\n<i><b>Note</b>: Telegram limitation for bots, bots can't delete 48h old messages...</i>")
        return

    try:
        sent_msg = await Message.send_msg(chat.id, f"Purge started...\nFrom: <a href='{reply.link}'>{reply.id}</a>\nTo: <a href='{e_msg.link}'>{e_msg.id}</a>")
        for msg_id in range(reply.id, e_msg.id+1):
            try:
                await Message.del_msg(chat.id, msg_id=msg_id)
            except Exception as e:
                logger.error(e)
        await Message.edit_msg(update, f"Purge completed!", sent_msg)
        await _log_channel(context, chat, user, action="MSG_PURGE")
    except Exception as e:
        logger.error(e)
        await Message.send_msg(chat.id, f"Error: {e}")
