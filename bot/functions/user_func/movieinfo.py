from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.omdb_info import fetch_movieinfo

async def func_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    movie_name = " ".join(context.args)

    if not movie_name:
        await effective_message.reply_text("Use <code>/movie movie name</code>\nE.g. <code>/movie animal</code>\nor\n<code>/movie -i tt13751694</code> [IMDB ID]\nor\n<code>/movie bodyguard -y 2011</code>")
        return
    
    if "-i" in movie_name and "-y" in movie_name:
        await effective_message.reply_text("⚠ You can't use both statement at once!\n/movie for details.")
        return
    
    imdb_id = None
    year = None
    
    if "-i" in movie_name:
        index_i = movie_name.index("-i")
        imdb_id = movie_name[index_i + len("-i"):].strip()
        movie_name = None
    elif "-y" in movie_name:
        index_y = movie_name.index("-y")
        year = movie_name[index_y + len("-y"):].strip()
        movie_name = movie_name[0: index_y].strip()

    movie_info = await fetch_movieinfo(movie_name=movie_name, imdb_id=imdb_id, year=year)
    if not movie_info:
        await effective_message.reply_text("Oops! Something went wrong!")
        return
    elif movie_info["Response"] == "False":
        await effective_message.reply_text("Invalid movie name!")
        return
    
    runtime = movie_info["Runtime"]
    runtime = f"{int(runtime[0:3]) // 60} Hour {int(runtime[0:3]) % 60} Min" if runtime != "N/A" else "N/A"

    text = (
        f"<b><a href='https://www.imdb.com/title/{movie_info.get('imdbID')}'>{movie_info.get('Title')} | {movie_info.get('imdbID')}</a></b>\n\n"
        f"<b>🎥 Content Type:</b> {movie_info.get('Type')}\n"
        f"<b>📄 Title:</b> {movie_info.get('Title')}\n"
        f"<b>👁‍🗨 Released:</b> {movie_info.get('Released')}\n"
        f"<b>🕐 Time:</b> {runtime}\n"
        f"<b>🎨 Genre:</b> {movie_info.get('Genre')}\n"
        f"<b>🤵‍♂️ Director:</b> {movie_info.get('Director')}\n"
        f"<b>🧑‍💻 Writer:</b> {movie_info.get('Writer')}\n"
        f"<b>👫 Actors:</b> {movie_info.get('Actors')}\n"
        f"<b>🗣 Language:</b> {movie_info.get('Language')}\n"
        f"<b>🌐 Country:</b> {movie_info.get('Country')}\n"
        f"<b>🏆 Awards:</b> {movie_info.get('Awards')}\n"
        f"<b>🎯 Meta Score:</b> {movie_info.get('Metascore')}\n"
        f"<b>🎯 IMDB Rating:</b> {movie_info.get('imdbRating')}\n"
        f"<b>📊 IMDB Votes:</b> {movie_info.get('imdbVotes')}\n"
        f"<b>🏷 IMDB ID:</b> <code>{movie_info.get('imdbID')}</code>\n"
        f"<b>💰 BoxOffice:</b> {movie_info.get('BoxOffice')}\n\n"
        f"<b>📝 Plot:</b>\n<blockquote>{movie_info.get('Plot')}</blockquote>\n"
    )

    photo = movie_info["Poster"]
    if photo:
        await effective_message.reply_photo(photo, text)
    else:
        await effective_message.reply_text(text)
