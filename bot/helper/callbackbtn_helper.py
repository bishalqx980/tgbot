from telegram import Update
from telegram.ext import ContextTypes


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "mp4":
        # importing from main.py
        from main import exe_func_ytdl
        url = context.user_data.get("url")
        extention = "mp4"
        await query.message.delete()
        await exe_func_ytdl(update, context, url, extention)
    elif data == "mp3":
        # importing from main.py
        from main import exe_func_ytdl
        url = context.user_data.get("url")
        extention = "mp3"
        await query.message.delete()
        await exe_func_ytdl(update, context, url, extention)
    elif data == "close":
        await query.message.delete()
