from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message

async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message

    if re_msg:
        if re_msg.forward_from:
            from_user_id = re_msg.forward_from.id
        elif re_msg.from_user:
            from_user_id = re_msg.from_user.id

    if chat.type == "private":
        if re_msg:
            if user.id == from_user_id:
                msg = (
                    f"• Your UserID: <code>{user.id}</code>\n"
                    f"<i>Replied user account is hidden! Can't get user_id</i>"
                )
            else:
                msg = (
                    f"• Your UserID: <code>{user.id}</code>\n"
                    f"• Replied UserID: <code>{from_user_id}</code>"
                )
        else:
            msg = (
                f"• UserID: <code>{user.id}</code>"
            )
        await Message.reply_msg(update, msg)

    elif chat.type in ["group", "supergroup"]:
        if re_msg:
            msg = (
                f"• Your UserID: <code>{user.id}</code>\n"
                f"• Replied UserID: <code>{from_user_id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            ) 
        else:
            msg = (
                f"• UserID: <code>{user.id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            )
        await Message.reply_msg(update, msg)
