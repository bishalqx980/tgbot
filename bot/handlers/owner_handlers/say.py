from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    re_msg = message.reply_to_message
    speech = " ".join(context.args) # the sentence to say
    
    try:
        await message.delete()
    except Exception as e:
        await message.reply_text(str(e))
        return
    
    if not speech:
        await message.reply_text("What should I say? Example: <code>/say Hi</code>")
        return
    
    await message.reply_text(speech, reply_to_message_id=re_msg.message_id if re_msg else None)
