from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.omdb_movie_info import get_movie_info


async def func_movieinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/movie movie_name</code>\nE.g. <code>/movie animal</code>\nor\n<code>/movie -i tt13751694</code> [IMDB ID]\nor\n<code>/movie bodyguard -y 2011</code>")
        return
    
    if "-i" in msg and "-y" in msg:
        await Message.reply_msg(update, "⚠ You can't use both statement in same message!\n/movie for details.")
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
    
    if not movie_info:
        await Message.send_msg(chat.id, "Movie name invalid!")
        return
    
    if movie_info == False:
        await Message.send_msg(chat.id, "omdb_api not found!")
        return

    poster, content_type, title, released, runtime, genre, director, writer, actors, plot, language, country, awards, meta_score, imdb_rating, imdb_votes, imdb_id, box_office = movie_info

    movie_info_dict = {
        "🎥 Content Type": content_type,
        "📄 Title": title,
        "👁‍🗨 Released": released,
        "🕐 Time": runtime,
        "🎨 Genre": genre,
        "🤵‍♂️ Director": director,
        "🧑‍💻 Writer": writer,
        "👫 Actors": actors,
        "🗣 Language": language,
        "🌐 Country": country,
        "🏆 Awards": awards,
        "🎯 Meta Score": meta_score,
        "🎯 IMDB Rating": imdb_rating,
        "📊 IMDB Votes": imdb_votes,
        "🏷 IMDB ID": f"<code>{imdb_id}</code>",
        "💰 BoxOffice": box_office
    }

    msg = "<b>Movie Information:</b>\n\n"
    for key, value in movie_info_dict.items():
        msg += f"<b>{key}:</b> {value}\n"
    
    msg += f"\n<b>📝 Plot:</b>\n<blockquote>{plot}</blockquote>\n"

    btn_data = {
        f"IMDB - {title}": f"https://www.imdb.com/title/{imdb_id}"
    }
    btn = await Button.ubutton(btn_data)

    await Message.send_img(chat.id, poster, msg, btn=btn)
