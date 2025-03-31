from telegram import Update
from telegram.ext import ContextTypes
from bot.functions.sudo_users import fetch_sudos

async def func_say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    speech = " ".join(context.args) # the sentence to say

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    try:
        await effective_message.delete()
    except Exception as e:
        await effective_message.reply_text(str(e))
        return
    
    if not speech:
        await effective_message.reply_text("What should I say? Example: <code>/say Hi</code>")
        return
    
    await effective_message.reply_text(speech, reply_to_message_id=re_msg.message_id if re_msg else None)
