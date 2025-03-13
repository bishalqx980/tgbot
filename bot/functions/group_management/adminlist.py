from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.functions.group_management.auxiliary_func.pm_error import _pm_error



async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return

    

    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""

    admins = await bot.get_chat_administrators(chat.id)
    for admin in admins:
        custom_title = admin.custom_title if admin.custom_title else ""
        admin_name = "Ghost 👻" if admin.is_anonymous else admin.user.mention_html()
        formatted_msg = f"• {admin_name} - <i>{custom_title}</i>\n"

        if admin.status == "creator":
            owner_storage += formatted_msg
        elif not admin.user.is_bot:
            admins_storage += formatted_msg
        
    if admins_storage:
        admins_storage = f"\n<b>Admin's:</b>\n{admins_storage}"
    
    msg = (
        f"<b><u>{chat.title}</u></b>\n\n"
        f"{owner_storage}{admins_storage}"
    )

    await effective_message.reply_text(msg)
