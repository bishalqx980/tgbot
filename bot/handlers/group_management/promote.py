from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import logger
from .auxiliary.pm_error import pm_error
from .auxiliary.chat_admins import ChatAdmins
from .auxiliary.anonymous_admin import anonymousAdmin

async def func_promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    victim = re_msg.from_user if re_msg else None
    admintitle = " ".join(context.args)

    cmd_prefix = effective_message.text[1]
    is_silent = False
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if cmd_prefix == "s":
        is_silent = True
        try:
            await effective_message.delete()
        except:
            pass
    
    if user.is_bot:
        user = await anonymousAdmin(chat, effective_message)
        if not user:
            return
    
    if not re_msg:
        await effective_message.reply_text("I don't know who you are talking about! Reply the member whom you want to promote!\nE.g<code>/promote admin title</code>")
        return
    
    if victim.id == context.bot.id:
        await effective_message.reply_text("I wish I could promote myself!")
        return
    
    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, context.bot.id, user.id, victim.id)
    
    if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return

    if chat_admins.is_victim_admin or chat_admins.is_victim_owner:
        await effective_message.reply_text(f"{victim.mention_html()} is already an admin of this chat!")
        return
    
    if chat_admins.is_user_admin and not chat_admins.is_user_admin.can_promote_members:
        await effective_message.reply_text("You don't have enough permission to promote chat members!")
        return
    
    if not chat_admins.is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    if not chat_admins.is_bot_admin.can_promote_members:
        await effective_message.reply_text("I don't have enough permission to promote chat members!")
        return
    
    try:
        await chat.promote_member(victim.id, can_invite_users=True)
        if admintitle:
            await chat.set_administrator_custom_title(victim.id, admintitle)
    except Exception as e:
        logger.error(e)
        await effective_message.reply_text(str(e))
        return
    
    if not is_silent:
        text = f"{victim.mention_html()} has been promoted." + (f"\nTitle: {admintitle}" if admintitle else "")
        await effective_message.reply_text(text)
