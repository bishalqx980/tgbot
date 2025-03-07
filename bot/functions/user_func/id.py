from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import MessageOriginType
from bot.helper.telegram_helpers.telegram_helper import Message

async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    victim = None

    if re_msg:
        forward_origin = re_msg.forward_origin
        from_user = re_msg.from_user
    
        if forward_origin and forward_origin.type == MessageOriginType.USER:
            victim = forward_origin.sender_user
        
        if from_user and not forward_origin:
            victim = from_user
        
        if not victim:
            msg = (
                f"• {user.full_name}\n"
                f"  » <b>ID:</b> <code>{user.id}</code>\n"
                f"• {forward_origin.sender_user_name}\n"
                f"  » <b>ID:</b> <code>Replied user account is hidden!</code>\n"
                f"• <b>ChatID:</b> <code>{chat.id}</code>"
            )
        else:
            msg = (
                f"• {user.full_name}\n"
                f"  » <b>ID:</b> <code>{user.id}</code>\n"
                f"• {victim.full_name}\n"
                f"  » <b>ID:</b> <code>{victim.id}</code>\n"
                f"• <b>ChatID:</b> <code>{chat.id}</code>"
            )
    else:
        msg = (
            f"• {user.full_name}\n"
            f"  » <b>ID:</b> <code>{user.id}</code>\n"
            f"• <b>ChatID:</b> <code>{chat.id}</code>"
        )
    
    await Message.reply_message(update, msg)
