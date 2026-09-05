from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from bot.utils.decorators.pm_error import pm_error
from .auxiliary.anonymous_admin import anonymousAdmin


@pm_error
async def func_leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    
    if user.is_bot:
        user = await anonymousAdmin(chat, effective_message)
        if not user:
            return
    
    try:
        user_status = await chat.get_member(user.id)
    except Exception as e:
        await effective_message.reply_text(str(e))
        return

    if user_status.status not in [ChatMemberStatus.OWNER]:
        await effective_message.reply_text("Huh, you aren't the owner of this chat!")
        return
    
    await effective_message.reply_text(
        "Should I leave?",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Leave", callback_data=f"admin_leavechat_{user.id}"),
            InlineKeyboardButton("Stay", callback_data="misc_close")
        ]])
    )
