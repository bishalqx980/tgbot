from bot.helper import commands


class MessageStorage:
    async def welcome_msg():
        pvt_message = (
            "Hi {user_mention}! I'm <a href='https://t.me/{bot_username}'>{bot_firstname}</a>, your all-in-one bot!\n"
            "Here's what I can do:\n\n" # break
            "• Get response from <b><i>ChatGPT AI</i></b>\n"
            "• Generate image from your prompt\n"
            "• Download/Search videos from YouTube\n"
            "• Provide movie information\n"
            "• Translate languages\n"
            "• Encode/decode base64\n"
            "• Shorten URLs\n"
            "• Ping any URL\n"
            "• Be your calculator\n"
            "• Echo your message for fun\n"
            "• Take website screenshot\n"
            "• Provide weather information\n"
            "• Group management & Much more...\n"
            "• /help for bot help\n\n" # break
            "<i>More Feature coming soon...</i>\n"
        )
        group_message = (
            "Hi, {user_mention}! Start me in private to chat with me 😊!"
        )
        return pvt_message, group_message


    async def msg_movie_info(movie_info):
        # get_movie_info()
        message = (
            f"<b>🎥 Content Type:</b> {movie_info[1]}\n"
            f"<b>📄 Title:</b> {movie_info[2]}\n"
            f"<b>👁‍🗨 Released:</b> {movie_info[3]}\n"
            f"<b>🕐 Time:</b> {movie_info[4]}\n"
            f"<b>🎨 Genre:</b> {movie_info[5]}\n"
            f"<b>🤵‍♂️ Director:</b> {movie_info[6]}\n"
            f"<b>🧑‍💻 Writer:</b> {movie_info[7]}\n"
            f"<b>👫 Actors:</b> {movie_info[8]}\n" # plot len 9 at the last
            f"<b>🗣 Language:</b> {movie_info[10]}\n"
            f"<b>🌐 Country:</b> {movie_info[11]}\n"
            f"<b>🏆 Awards:</b> {movie_info[12]}\n"
            f"<b>🎯 Meta Score:</b> {movie_info[13]}\n"
            f"<b>🎯 IMDB Rating:</b> {movie_info[14]}\n"
            f"<b>📊 IMDB Votes:</b> {movie_info[15]}\n"
            f"<b>🏷 IMDB ID:</b> <code>{movie_info[16]}</code>\n"
            f"<b>💰 BoxOffice:</b> {movie_info[17]}\n\n" # break
            f"<b>📝 **Plot:</b>\n"
            f"<pre>{movie_info[9]}</pre>\n"
        )
        return message


    async def help_msg():
        message = "<b>Available Bot Command's</b>\n\n"
        for cmd in commands:
            message += (f"/{cmd.command} » <i>{cmd.description}</i>\n")
        return message
