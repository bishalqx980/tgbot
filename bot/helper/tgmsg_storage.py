class MsgStorage:
    def msg_movie_info(movie_info):
        # get_movie_info()
        message = (
            f"<b>🎥 Content Type:</b> {movie_info[1]}\n"
            f"<b>📄 Title:</b> {movie_info[2]}\n"
            f"<b>👁‍🗨 Released:</b> {movie_info[3]}\n"
            f"<b>🕐 Time:</b> {movie_info[4]}\n"
            f"<b>🎨 Genre:</b> {movie_info[5]}\n"
            f"<b>🤵‍♂️ Director:</b> {movie_info[6]}\n"
            f"<b>🧑‍💻 Writer:</b> {movie_info[7]}\n"
            f"<b>👫 Actors:</b> {movie_info[8]}\n"
            f"<b>📝 **Plot:</b>\n"
            f"<pre>{movie_info[9]}</pre>\n"
            f"<b>🗣 Language:</b> {movie_info[10]}\n"
            f"<b>🌐 Country:</b> {movie_info[11]}\n"
            f"<b>🏆 Awards:</b> {movie_info[12]}\n"
            f"<b>🎯 Meta Score:</b> {movie_info[13]}\n"
            f"<b>🎯 IMDB Rating:</b> {movie_info[14]}\n"
            f"<b>📊 IMDB Votes:</b> {movie_info[15]}\n"
            f"<b>🏷 IMDB ID:</b> <code>{movie_info[16]}</code>\n"
            f"<b>💰 BoxOffice:</b> {movie_info[17]}\n"
        )
        return message