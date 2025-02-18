from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.omdb_movie_info import get_movie_info


async def func_movieinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = " ".join(context.args)

    if not msg:
        await Message.reply_message(update, "Use <code>/movie movie_name</code>\nE.g. <code>/movie animal</code>\nor\n<code>/movie -i tt13751694</code> [IMDB ID]\nor\n<code>/movie bodyguard -y 2011</code>")
        return
    
    if "-i" in msg and "-y" in msg:
        await Message.reply_message(update, "⚠ You can't use both statement at once!\n/movie for details.")
        return
    
    imdb_id = None
    year = None
    
    if "-i" in msg:
        index_i = msg.index("-i")
        imdb_id = msg[index_i + len("-i"):].strip()
        msg = None
    elif "-y" in msg:
        index_y = msg.index("-y")
        year = msg[index_y + len("-y"):].strip()
        msg = msg[0:index_y].strip()

    movie_info = await get_movie_info(movie_name=msg, imdb_id=imdb_id, year=year)

    if movie_info == False:
        await Message.reply_message(update, "omdb_api not found!")
        return
    elif not movie_info:
        await Message.reply_message(update, "Oops! Please try again or report the issue.")
        return
    elif movie_info["Response"] == "False":
        await Message.reply_message(update, "Invalid movie name!")
        return
    
    runtime = movie_info["Runtime"]
    runtime = f"{int(runtime[0:3]) // 60} Hour {int(runtime[0:3]) % 60} Min"

    msg = (
        f"<b><a href='https://www.imdb.com/title/{movie_info['imdbID']}'>{movie_info['Title']} | {movie_info['imdbID']}</a></b>\n\n"
        f"<b>🎥 Content Type:</b> {movie_info['Type']}\n"
        f"<b>📄 Title:</b> {movie_info['Title']}\n"
        f"<b>👁‍🗨 Released:</b> {movie_info['Released']}\n"
        f"<b>🕐 Time:</b> {runtime}\n"
        f"<b>🎨 Genre:</b> {movie_info['Genre']}\n"
        f"<b>🤵‍♂️ Director:</b> {movie_info['Director']}\n"
        f"<b>🧑‍💻 Writer:</b> {movie_info['Writer']}\n"
        f"<b>👫 Actors:</b> {movie_info['Actors']}\n"
        f"<b>🗣 Language:</b> {movie_info['Language']}\n"
        f"<b>🌐 Country:</b> {movie_info['Country']}\n"
        f"<b>🏆 Awards:</b> {movie_info['Awards']}\n"
        f"<b>🎯 Meta Score:</b> {movie_info['Metascore']}\n"
        f"<b>🎯 IMDB Rating:</b> {movie_info['imdbRating']}\n"
        f"<b>📊 IMDB Votes:</b> {movie_info['imdbVotes']}\n"
        f"<b>🏷 IMDB ID:</b> <code>{movie_info['imdbID']}</code>\n"
        f"<b>💰 BoxOffice:</b> {movie_info['BoxOffice']}\n\n"
        f"<b>📝 Plot:</b>\n<blockquote>{movie_info['Plot']}</blockquote>\n"
    )

    await Message.send_image(chat.id, movie_info["Poster"], msg)
