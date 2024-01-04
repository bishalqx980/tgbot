import asyncio
from pytube import YouTube
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters



async def ytdl(url):
    try:
        yt = YouTube(url)
        title = yt.title
        file_type = "audio"
        extention = "mp3"
        order_by = "abr"
        file_path = "ytdl/download/"

        stream = (
            yt.streams
            .filter(type=file_type)
            .order_by(order_by)
            .desc()
            .first()
        )
        if stream:
            filename = f"video.{extention}"
            file_path = stream.download(output_path=file_path, filename=filename)
            return title, file_path
        else:
            print("No stream found for this video")
    except Exception as e:
        print(f"Error ytdl: {e}")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    await update.message.reply_text(f'Loading...')
    url = " ".join(context.args)
    res = await ytdl(url)
    audio_file = open(res[1], "rb")
    if audio_file:
        await context.bot.send_audio(chat_id=chat.id, audio=audio_file, title=res[0], caption=res[0])


app = ApplicationBuilder().token("6734963977:AAE2y_gfEULKMK8uMn7hmucQzNJDV6bdRbk").build()

app.add_handler(CommandHandler("ytdl", send))

app.run_polling()