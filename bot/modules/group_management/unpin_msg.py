from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.check_del_cmd import _check_del_cmd
from bot.modules.group_management.check_permission import _check_permission


async def func_unpin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None
    msg = " ".join(context.args)
    
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
    
    if msg == "all":
        if user_permission.status != ChatMember.OWNER:
            await Message.reply_msg(update, "❌ This command is only for chat owner!")
            return
        
        context.chat_data["chat_id"] = chat.id
        context.chat_data["user_id"] = user.id
        context.chat_data["del_msg_pointer"] = e_msg
        
        btn_name = ["⚠ YES", "🍀 NO"]
        btn_data = ["unpin_all", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)
        try:
            await Message.reply_msg(update, f"Do you really want to unpin all messages of this chat?", btn)
            await _log_channel(context, chat, user, action="UNPIN_ALL")
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat.id, f"Error: {e}")
        return

    if not reply:
        await Message.reply_msg(update, "This command will unpin replied message!\nUse <code>/unpin all</code> to unpin all pinned messages of chat!")
        return
    
    try:
        await bot.unpin_chat_message(chat.id, msg_id)
        await Message.reply_msg(update, f"Message unpinned!")
        await _log_channel(context, chat, user, action="UNPIN")
    except Exception as e:
        logger.error(e)
        await Message.send_msg(chat.id, f"Error: {e}")
