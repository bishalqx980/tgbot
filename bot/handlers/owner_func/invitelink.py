import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ..sudo_users import fetch_sudos

async def func_invitelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    chat_id = " ".join(context.args)

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([effective_message.id, sent_message.id])
        return
    
    if not chat_id:
        await effective_message.reply_text("<code>/invitelink ChatID</code> to get specified chat invite link.\n<i>Note: only works if this bot is in that chat and have enough permissions to get invite link!</i>")
        return
    
    sent_message = await effective_message.reply_text("Please wait...")
    expire_date = datetime.now() + timedelta(days=1) # expire after 1day of creation

    try:
        invite_link = await context.bot.create_chat_invite_link(chat_id, expire_date, 1)
    except Exception as e:
        await sent_message.edit_text(str(e))
        return
    
    await sent_message.edit_text(f"<b>Generated link:</b> {invite_link.invite_link}")
