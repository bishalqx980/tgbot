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
    
    if "-i" and "-y" in msg:
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
    
    if movie_info == 0:
        await Message.send_msg(chat.id, "omdb_api not found!")
        return

    poster, content_type, title, released, runtime, genre, director, writer, actors, plot, language, country, awards, meta_score, imdb_rating, imdb_votes, imdb_id, box_office = movie_info
    
    msg = (
        f"<b>🎥 Content Type:</b> {content_type}\n"
        f"<b>📄 Title:</b> {title}\n"
        f"<b>👁‍🗨 Released:</b> {released}\n"
        f"<b>🕐 Time:</b> {runtime}\n"
        f"<b>🎨 Genre:</b> {genre}\n"
        f"<b>🤵‍♂️ Director:</b> {director}\n"
        f"<b>🧑‍💻 Writer:</b> {writer}\n"
        f"<b>👫 Actors:</b> {actors}\n" # plot len 9 at the last
        f"<b>🗣 Language:</b> {language}\n"
        f"<b>🌐 Country:</b> {country}\n"
        f"<b>🏆 Awards:</b> {awards}\n"
        f"<b>🎯 Meta Score:</b> {meta_score}\n"
        f"<b>🎯 IMDB Rating:</b> {imdb_rating}\n"
        f"<b>📊 IMDB Votes:</b> {imdb_votes}\n"
        f"<b>🏷 IMDB ID:</b> <code>{imdb_id}</code>\n"
        f"<b>💰 BoxOffice:</b> {box_office}\n\n" # break
        f"<b>📝 **Plot:</b>\n"
        f"<blockquote>{plot}</blockquote>\n"
    )

    btn_name = [f"IMDB - {title}"]
    btn_url = [f"https://www.imdb.com/title/{imdb_id}"]
    btn = await Button.ubutton(btn_name, btn_url)

    await Message.send_img(chat.id, poster, msg, btn)
