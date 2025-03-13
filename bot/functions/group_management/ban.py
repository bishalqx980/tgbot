from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from bot.functions.group_management.auxiliary_func.pm_error import pm_error

async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    victim = re_msg.from_user if re_msg else None
    reason = " ".join(context.args)
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? Ghost? Sorry, I don't take commands from Ghost's. 👻")
        return
    
    if not re_msg:
        await effective_message.reply_text("I don't know who you are talking about 🤔! Reply the member whom you want to ban! To mention with reason <code>/ban reason</code>")
        return
    
    if victim.id == context.bot.id:
        await effective_message.reply_text("I'm not going to ban myself! 😑")
        return
    
    chat_admins = await chat.get_administrators()

    is_user_admin = None
    is_user_owner = None

    is_victim_admin = None
    is_victim_owner = None

    is_bot_admin = None

    for admin in chat_admins:
        admin_id = admin.user.id
        admin_status = admin.status

        if admin_id == user.id:
            if admin_status == ChatMember.ADMINISTRATOR:
                is_user_admin = admin
            elif admin_status == ChatMember.OWNER:
                is_user_owner = admin
        
        elif admin_id == victim.id:
            if admin_status == ChatMember.ADMINISTRATOR:
                is_victim_admin = admin
            elif admin_status == ChatMember.OWNER:
                is_victim_owner = admin
        
        elif admin_id == context.bot.id:
            is_bot_admin = admin

        if is_user_admin is not None and is_user_owner is not None and is_victim_admin is not None and is_victim_owner is not None and is_bot_admin is not None:
            break
    
    if not (is_user_admin or is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if is_user_owner and is_victim_admin:
        pass

    elif is_user_admin and (is_victim_admin or is_victim_owner):
        await effective_message.reply_text("I'm not going to ban an admin! You must be kidding!")
        return
    
    if is_user_admin and not is_user_admin.can_restrict_members:
        await effective_message.reply_text("You don't have enough rights to restrict chat members!")
        return
    
    if not is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not is_bot_admin.can_restrict_members:
        await effective_message.reply_text("I don't have enough rights to restrict chat members!")
        return
    
    try:
        await chat.ban_member(victim.id)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    await effective_message.reply_text(f"{victim.name} has been banned from this chat.")
    
#     if is_silent:
#         await Message.delete_message(chat.id, sent_msg)
#     else:
#         msg = f"{victim.mention_html()} has been banned in this chat!\n<b>Admin:</b> {user.first_name}"
#         if reason:
#             msg = f"{msg}\n<b>Reason</b>: {reason}"
        
#         await effective_message.reply_text(msg, sent_msg)

#     # send message to banned user private chat
#     msg = f"{user.mention_html()} has banned you in {chat.title}!"
#     if reason:
#         msg = f"{msg}\n<b>Reason</b>: {reason}"
    
#     await Message.send_message(victim.id, msg)


# async def func_sban(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat = update.effective_chat
#     effective_message = update.effective_message
    
#     await Message.delete_message(chat.id, e_msg)
#     await func_ban(update, context, is_silent=True)
