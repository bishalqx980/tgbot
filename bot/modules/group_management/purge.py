import asyncio
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_purge(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None, purgefrom_id=None):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_message(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

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
        if not user_permission.can_delete_messages:
            await Message.reply_message(update, "You don't have enough rights to delete chat messages!")
            return
    
    if not bot_permission.can_delete_messages:
        await Message.reply_message(update, "I don't have enough rights to delete chat messages!")
        return
    
    if not reply:
        await Message.reply_message(update, "I don't know which message to delete from! Reply the message that you want to start delete from!\n\n<i><b>Note:</b> bots are unable to delete 48h old messages due to Telegram limitation/restriction...</i>")
        return
    
    sent_msg = await Message.send_message(chat.id, f"Purge started...")

    if purgefrom_id:
        while purgefrom_id <= reply.id:
            await Message.delete_message(chat.id, purgefrom_id)
            purgefrom_id += 1
    else:
        await asyncio.gather(*(Message.delete_message(chat.id, msg_id) for msg_id in range(reply.id, e_msg.id + 1)))

    if is_silent:
        await Message.delete_message(chat.id, sent_msg)
    else:
        await Message.edit_message(update, f"Purge completed!", sent_msg)
    await _log_channel(update, chat, user, action="MSG_PURGE")


async def func_spurge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    await Message.delete_message(chat.id, e_msg)
    await func_purge(update, context, is_silent=True)


async def func_purgefrom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    reply = update.message.reply_to_message
    e_msg = update.effective_message

    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    if not reply:
        await Message.reply_message(update, "Reply the message with /purgefrom which message you want to purge from! Then reply the message with /purgeto where to stop purge!")
        return
    
    await LOCAL_DATABASE.insert_data("data_center", chat.id, {"purgefrom_id": reply.id})
    sent_msg = await Message.reply_message(update, "<code>purgefrom</code> added...")
    await asyncio.sleep(5)
    for del_msg in [e_msg, sent_msg]:
        await Message.delete_message(chat.id, del_msg)


async def func_purgeto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message

    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    purgefrom_id = None
    localdb = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if localdb:
        purgefrom_id = localdb.get("purgefrom_id")
    
    if not purgefrom_id:
        await Message.reply_message(update, "Reply the message with /purgefrom which message you want to purge from! Then reply the message with /purgeto where to stop purge!")
        return
    
    await LOCAL_DATABASE.insert_data("data_center", chat.id, {"purgefrom_id": None})
    await func_purge(update, context, purgefrom_id=purgefrom_id)
    await asyncio.sleep(5)
    await Message.delete_message(chat.id, e_msg)
