from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.shrinkme import shortener_url


async def func_shortener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    url = (re_msg.text or re_msg.caption) if re_msg else " ".join(context.args)

    if not url:
        await Message.reply_message(update, "Use <code>/short url</code>\nor reply the url with <code>/short</code> command.\nE.g. <code>/short https://google.com</code>")
        return
    
    shorted_url = await shortener_url(url)
    if shorted_url == False:
        msg = "shrinkme_api not found!"
    elif not shorted_url:
        msg = "Oops! Please try again or report the issue. (invalid url? 🤔)"
    else:
        msg = shorted_url

    await Message.reply_message(update, msg)
