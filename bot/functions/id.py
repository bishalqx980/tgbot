from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message

async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message

    if re_msg:
        if re_msg.forward_from:
            from_user = re_msg.forward_from
        elif re_msg.from_user:
            from_user = re_msg.from_user

    if chat.type == "private":
        if re_msg:
            if user.id == from_user.id:
                msg = (
                    f"• {user.full_name}\n"
                    f"  » <b>ID:</b> <code>{user.id}</code>\n"
                    f"<i>Replied user account is hidden!</i>"
                )
            else:
                msg = (
                    f"• {user.full_name}\n"
                    f"  » <b>ID:</b> <code>{user.id}</code>\n"
                    f"• {from_user.full_name}\n"
                    f"  » <b>ID:</b> <code>{from_user.id}</code>\n"
                )
        else:
            msg = (
                f"• {user.full_name}\n"
                f"  » <b>ID:</b> <code>{user.id}</code>"
            )
        
        await Message.reply_msg(update, msg)

    elif chat.type in ["group", "supergroup"]:
        if re_msg:
            msg = (
                f"• {user.full_name}\n"
                f"  » <b>ID:</b> <code>{user.id}</code>\n"
                f"• {from_user.full_name}\n"
                f"  » <b>ID:</b> <code>{from_user.id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            )
        else:
            msg = (
                f"• {user.full_name}\n"
                f"  » <b>ID:</b> <code>{user.id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            )
        
        await Message.reply_msg(update, msg)
