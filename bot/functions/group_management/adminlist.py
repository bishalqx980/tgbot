from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.functions.group_management.auxiliary.pm_error import pm_error

async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return

    owner = "<b>Owner:</b>\n"
    admins = ""

    chat_admins = await chat.get_administrators()

    for admin in chat_admins:
        custom_title = f"- <i>{admin.custom_title}</i>" if admin.custom_title else ""
        admin_name = "Anonymous" if admin.is_anonymous else admin.user.mention_html()
        formatted_text = f"• {admin_name} {custom_title}\n"

        if admin.status == ChatMember.OWNER:
            owner += formatted_text
        elif not admin.user.is_bot:
            admins += formatted_text
        
    if admins:
        admins = f"\n<b>Admin's:</b>\n{admins}"
    
    text = (
        f"<blockquote>{chat.title}</blockquote>\n\n"
        f"{owner}{admins}"
    )

    await effective_message.reply_text(text)
