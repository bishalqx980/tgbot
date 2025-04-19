from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

async def conv_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # refined query data
    query_data = query.data.removeprefix("conv_")

    if query_data == "cancel":
        await query.edit_message_text("Okay, Reporting cancelled.")
        return ConversationHandler.END
