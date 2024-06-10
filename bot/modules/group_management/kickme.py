from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.group_management.check_del_cmd import _check_del_cmd
from bot.modules.group_management.check_permission import _check_permission


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await _check_del_cmd(update, context)

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if not bot_permission.can_restrict_members:
        await Message.reply_msg(update, "I don't have enough rights to restrict/unrestrict chat member!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to kick you! You must be joking!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"Nice Choice! Get out of my sight!\n{victim.mention_html()} has choosed the easy way to out!")
        await bot.unban_chat_member(chat.id, victim.id)
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            await Message.send_msg(victim.id, f"You kicked yourself from {chat.title}!\nInvite Link: {invite_link.invite_link}")
        except Exception as e:
            logger.error(e)
    except Exception as e:
        logger.error(e)
        await Message.send_msg(chat.id, f"Error: {e}")
