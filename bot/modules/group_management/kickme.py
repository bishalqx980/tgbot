from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

    sent_msg = await Message.reply_message(update, "💭")
    _chk_per = await _check_permission(update, victim, user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
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
