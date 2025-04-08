from telegram import Update
from telegram.ext import ContextTypes
from ...modules.shrinkme import shortener_url

async def func_shorturl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    url = (re_msg.text or re_msg.caption) if re_msg else " ".join(context.args)

    if not url:
        await effective_message.reply_text("Use <code>/shorturl url</code>\nor reply the url with <code>/shorturl</code> command.\nE.g. <code>/shorturl https://google.com</code>")
        return
    
    shorted_url = await shortener_url(url)
    text = "Oops! Something went wrong!" if not shorted_url else shorted_url
    await effective_message.reply_text(text)
