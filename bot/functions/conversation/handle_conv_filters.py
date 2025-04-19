from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot import config

async def conv_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    await context.bot.send_message(
        config.owner_id,
        f"UserID: <code>{user.id}</code>\n"
        f"ChatID: <code>{chat.id}</code>\n\n"
        f"<blockquote>Report: {effective_message.text_html}</blockquote>"
    )

    await effective_message.reply_text("Report has been submitted. Our team will contact you as soon as possible.")

    return ConversationHandler.END
