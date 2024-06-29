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
    bots_storage = ""
      
    admins = await bot.get_chat_administrators(chat.id)
    for admin in admins:
        custom_title = f"- {admin.custom_title}" if admin.custom_title else ""
        if admin.status == "creator":
            if admin.is_anonymous == True:
                owner_storage += f"» Ghost 👻 <i>{custom_title}</i>\n"
            else:
                owner_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
        elif admin.user.is_bot == True:
            bots_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
        else:
            if admin.is_anonymous == True:
                admins_storage += f"» Ghost 👻 <i>{custom_title}</i>\n"
            else:
                admins_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
    if admins_storage:
        admins_storage = f"\n<b>Admin's:</b>\n{admins_storage}"
    if bots_storage:
        bots_storage = f"\n<b>Bot's:</b>\n{bots_storage}"

    await Message.reply_msg(update, f"<b>{chat.title}</b>\n▬▬▬▬▬▬▬▬▬▬\n{owner_storage}{admins_storage}{bots_storage}")
