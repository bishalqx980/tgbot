import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_cadmins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    chat_id = " ".join(context.args)
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([message.id, sent_message.id])
        return
    
    if not chat_id:
        await message.reply_text("<code>/cadmins ChatID</code> to get specified chat admin list.\n<i>Note: only works if this bot is in that chat!</i>")
        return
    
    sent_message = await message.reply_text("Please wait...")
    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""

    try:
        admins = await context.bot.get_chat_administrators(chat_id)
    except Exception as e:
        await sent_message.edit_text(str(e))
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
    
    text = (
        f"Admins of <code>{chat_id}</code>\n\n"
        f"{owner_storage}{admins_storage}"
    )

    await sent_message.edit_text(text)
