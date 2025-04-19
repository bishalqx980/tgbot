from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot import config
from bot.modules.database import MemoryDB

async def conv_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message

    await context.bot.send_message(config.owner_id, f"UserID: <code>{user.id}</code>\n\n<blockquote>{effective_message.text_html}</blockquote>")

    await effective_message.reply_text("Report has been submitted. Support team will contact you as soon as possible.")

    # Editing the previous message contains button
    data_center = MemoryDB.data_center.get(user.id)
    if not data_center:
        return
    
    await context.bot.edit_message_text(data_center["support_message"], user.id, data_center["support_message_id"])

    return ConversationHandler.END
