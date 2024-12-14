from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.archive.ytdl import PYTUBE


async def func_yts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = " ".join(context.args)

    if not keyword:
        await Message.reply_msg(update, "Use <code>/yts keyword</code>\nE.g. <code>/yts google keynote</code>")
        return
    
    result = await PYTUBE.yts(keyword)
    if not result:
        await Message.reply_msg(update, "Oops, something went wrong...")  
        return
    
    urls = [
        result[0].watch_url,
        result[1].watch_url,
        result[2].watch_url
    ]
    
    for url in urls:
        await Message.reply_msg(update, url, disable_web_preview=False)
    await Message.reply_msg(update, f"Video found: {len(result)}\nShowing top {len(urls)} videos!\nTo download videos you can use /ytdl")
