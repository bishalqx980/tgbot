from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger


from bot.functions.group_management.auxiliary_func.pm_error import _pm_error

from bot.functions.group_management.check_permission import _check_permission


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return

    

    sent_message = await effective_message.reply_text("💭")
    _chk_per = await _check_permission(update, victim, user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Something went wrong!", sent_msg)
        return
    
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
        return
    
    if not _chk_per["bot_permission"].can_restrict_members:
        await Message.edit_message(update, "I don't have enough rights to restrict/unrestrict chat member!", sent_msg)
        return
    
    if _chk_per["victim_permission"].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.edit_message(update, f"I'm not going to kick you! You must be joking!", sent_msg)
        return
    
    try:
        await bot.unban_chat_member(chat.id, victim.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_message(update, str(e), sent_msg)
        return

    await Message.edit_message(update, f"Nice Choice! Get out of my sight!\n{victim.mention_html()} has chosen the easy way to out!", sent_msg)

    # Send message to victim
    if chat.link:
        invite_link = chat.link
    else:
        try:
            create_invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            invite_link = create_invite_link.invite_link
        except Exception as e:
            logger.error(e)
            return
    
    await Message.send_message(victim.id, f"You kicked yourself from {chat.title}!\nYou can join again using this invite link!\nInvite Link: {invite_link}")
