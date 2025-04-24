from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.chat_admins import ChatAdmins

async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE, is_silent=None):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    victim = re_msg.from_user if re_msg else None
    reason = " ".join(context.args)
    mad_quote = "Huh! Do you know? Overthinking is just as bad as underthinking."
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    if not re_msg:
        await effective_message.reply_text("I don't know who you are talking about! Reply the member whom you want to unmute!\nE.g<code>/unmute reason</code>")
        return
    
    if victim.id == context.bot.id:
        await effective_message.reply_text(mad_quote)
        return
    
    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, context.bot.id, user.id, victim.id)
    
    if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return

    if chat_admins.is_victim_admin or chat_admins.is_victim_owner:
        await effective_message.reply_text(mad_quote)
        return
    
    if chat_admins.is_user_admin and not chat_admins.is_user_admin.can_restrict_members:
        await effective_message.reply_text("You don't have enough permission to unrestrict chat members!")
        return
    
    if not chat_admins.is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins.is_bot_admin.can_restrict_members:
        await effective_message.reply_text("I don't have enough permission to unrestrict chat members!")
        return
    
    try:
        await chat.restrict_member(victim.id, ChatPermissions.all_permissions())
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        text = f"{victim.mention_html()} has been unmuted." + (f"\nReason: {reason}" if reason else "")
        await effective_message.reply_text(text)


async def func_sunmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()
    await func_unmute(update, context, is_silent=True)
