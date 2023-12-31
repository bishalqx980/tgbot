from bot.helper import commands

class MessageStorage:
    def welcome_msg():
        pvt_message = (
            "Hi, {user_mention} !! It's <a href='https://t.me/{bot_username}'>{bot_firstname}</a>!\n"
            "I'm not only a Powerful <b>Group Management bot</b> but also\n"
            "I can do many other task 😜\n\n" # break
            "🔥 I can get response from <b>ChatGPT AI</b>\n\n" # break
            "⪧ I can get any Movie information\n"
            "⪧ I can Translate any language to your desired lang\n"
            "⪧ I can decode/encode base64 code\n"
            "⪧ I can short any URL\n"
            "⪧ I can ping (Detect web response) any URL\n"
            "⪧ You can use me as a calculator too 😎\n"
            "⪧ I can echo your message (for fun) 😁\n"
            "⪧ I can take screenshot of any website by url 📸\n\n" # break
            "🆘 More Feature coming soon...\n"
            "⪧ /help for bot help\n"
            "∞ Successor of <a href='https://t.me/YmlzaGFsbot'>Melina</a> ☺"
        )
        group_message = (
            "Hi, {user_mention}! Start me in private to chat with me 😊!"
        )
        return pvt_message, group_message


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


    def help_msg():
        message = "<b>Available Bot Commands ⚜</b>\n\n"
        for cmd in commands:
            message += (f"/{cmd.command} <code>: {cmd.description}</code>\n")
        return message
    