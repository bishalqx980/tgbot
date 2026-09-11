from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.modules.api.omdb import fetch_movieinfo
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "movieinfo",
    "commands": ["movie", "imdb"], # list of commands including aliases

    "description": (
        "Get IMDB information for specified movie.\n"
        "> **Example Usage**\n"
        "- **Movie Name :** `/imdb animal`\n"
        "- **IMDB ID :** `/imdb -i tt13751694`\n"
        "- **Specific Year :** `/imdb bodyguard -y 2011`"
    ),
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Movie Info", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    args = CommandArgs(message.text, message.command)

    if not args:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    if "-i" in args and "-y" in args:
        return await message.reply(
            "⚠ You can't use both parameter at once!\n"
            f"/{message.command[0]} for details."
        )
    
    imdb_id = None
    year = None
    
    if "-i" in args:
        imdb_id = args[args.index("-i") + len("-i"):].strip()
        movie_name = None
    
    elif "-y" in args:
        year = args[args.index("-y") + len("-y"):].strip()
        movie_name = args[0: args.index("-y")].strip()

    else:
        movie_name = args

    movie_info = await fetch_movieinfo(movie_name, imdb_id, year)

    if not movie_info:
        return await message.reply(
            "Error: Hmm, Something is wrong here, but I don't know!!"
        )

    # API Error
    elif movie_info["Response"] == "False":
        return await message.reply("Error: Invalid movie name!")
    
    runtime = movie_info["Runtime"]
    runtime = f"{int(runtime[0:3]) // 60} Hour {int(runtime[0:3]) % 60} Min" if runtime != "N/A" else "N/A"

    text = (
        f"**<a href='https://www.imdb.com/title/{movie_info.get('imdbID')}'>{movie_info.get('Title')} | {movie_info.get('imdbID')}</a>**\n\n"
        f"**🎥 Content Type:** {movie_info.get('Type')}\n"
        f"**📄 Title:** {movie_info.get('Title')}\n"
        f"**👁‍🗨 Released:** {movie_info.get('Released')}\n"
        f"**🕐 Time:** {runtime}\n"
        f"**🎨 Genre:** {movie_info.get('Genre')}\n"
        f"**🤵‍♂️ Director:** {movie_info.get('Director')}\n"
        f"**🧑‍💻 Writer:** {movie_info.get('Writer')}\n"
        f"**👫 Actors:** {movie_info.get('Actors')}\n"
        f"**🗣 Language:** {movie_info.get('Language')}\n"
        f"**🌐 Country:** {movie_info.get('Country')}\n"
        f"**🏆 Awards:** {movie_info.get('Awards')}\n"
        f"**🎯 Meta Score:** {movie_info.get('Metascore')}\n"
        f"**🎯 IMDB Rating:** {movie_info.get('imdbRating')}\n"
        f"**📊 IMDB Votes:** {movie_info.get('imdbVotes')}\n"
        f"**🏷 IMDB ID:** `{movie_info.get('imdbID')}`\n"
        f"**💰 BoxOffice:** {movie_info.get('BoxOffice')}\n\n"
        f"<blockquote expandable>**📝 Plot:** {movie_info.get('Plot')}</blockquote>"
    )

    photo = movie_info["Poster"]
    if photo:
        await message.reply_photo(photo, text)
    else:
        await message.reply(text)
