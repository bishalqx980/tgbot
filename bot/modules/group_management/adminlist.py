from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command


async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return

    await func_del_command(update, context)

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

    await Message.reply_message(update, msg)
