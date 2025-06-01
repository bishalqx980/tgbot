import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ChatType
from bot import logger, config

class SUPPORT_STATES:
    STATE_ONE = range(1)


async def init_support_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    text = (
        "Hey, please send your request/report in one message.\n"
        "• /cancel to cancel conversation.\n\n"
        "<blockquote><b>Note:</b> Request/Report should be related to this bot. And we don't provide any support for ban, mute or other things related to groups managed by this bot.</blockquote>"
    )

    await effective_message.reply_text(text)
    return SUPPORT_STATES.STATE_ONE


async def support_state_one(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message

    try:
        message = (
            f"Name: {user.mention_html()}\n"
            f"UserID: <code>{user.id}</code>\n"
            f"Message: <blockquote>{effective_message.text_html}</blockquote>"
        )

        await context.bot.send_message(config.owner_id, message)
        text = "Report has been submitted. Support team will contact you as soon as possible."
    except Exception as e:
        logger.error(e)
        text = "Oops, Something went wrong. Please try again."

    await effective_message.reply_text(text)
    return ConversationHandler.END


async def cancel_support_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Okay, Reporting cancelled.")
    return ConversationHandler.END
