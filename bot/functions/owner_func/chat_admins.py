import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import bot
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.functions.power_users import _power_users

async def func_chat_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    chat_id = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await Message.reply_message(update, f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not chat_id:
        await Message.reply_message(update, "<code>/chatadmins chat_id</code> to get specified chat adminlist.\n<i>Note: only works if this bot is in that chat!</i>")
        return
    
    sent_msg = await Message.reply_message(update, "Please wait...")
    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""

    try:
        admins = await bot.get_chat_administrators(chat_id)
    except Exception as e:
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    for admin in admins:
        custom_title = admin.custom_title if admin.custom_title else ""
        formatted_msg = f"• {admin.user.mention_html()} - <i>{custom_title}</i>\n"

        if admin.status == "creator":
            owner_storage += formatted_msg
        elif not admin.user.is_bot:
            admins_storage += formatted_msg
        
    if admins_storage:
        admins_storage = f"\n<b>Admin's:</b>\n{admins_storage}"
    
    msg = (
        f"Admins of <code>{chat_id}</code>\n\n"
        f"{owner_storage}{admins_storage}"
    )

    await Message.edit_message(update, msg, sent_msg)
