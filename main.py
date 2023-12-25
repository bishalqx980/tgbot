import asyncio
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot import bot_token, bot, owner_id, owner_username, server_url
from bot.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.ping import ping_url
from bot.shortener import shortener_url
from bot.translator import translate
from bot.base64 import decode_b64, encode_b64
from bot.omdb_movie_info import get_movie_info
from bot.utils import calc
from bot.helper.tgmsg_storage import MessageStorage


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    bot_info = await bot.get_me()
    avatar = MongoDB.get_data("ciri_docs", "avatar")

    welcome_msg = MessageStorage.welcome_msg()
    welcome_msg = welcome_msg.format(
        user_mention = user.mention_html(),
        bot_username = bot_info.username,
        bot_firstname = bot_info.first_name
    )

    btn = [
        [
            InlineKeyboardButton("⚡ Developer ⚡", f"https://t.me/{owner_username}")
        ]
    ]

    await Message.send_img(chat.id, avatar, welcome_msg, btn)

    if chat.type == "private":
        data = {
            "user_id": user.id,
            "Name": user.full_name,
            "username": user.username,
            "mention": user.mention_html(),
            "lang": user.language_code
        }
        find_db = MongoDB.find_one("users", "user_id", user.id)
        if not find_db:
            MongoDB.insert_single_data("users", data)


async def func_movieinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)

    if msg != "":
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
        elif "-i" and "-y" in msg:
            await Message.reply_msg(update, "⚠ You can't use both statement in same message!\n/movie for details.")

        movie_info = get_movie_info(movie_name=msg, imdb_id=imdb_id, year=year)
        if movie_info:
            msg = MessageStorage.msg_movie_info(movie_info)
            btn = [
                [InlineKeyboardButton(f"✨ IMDB - {movie_info[2]}", f"https://www.imdb.com/title/{movie_info[16]}")]
            ]
            await Message.send_img(update.effective_chat.id, movie_info[0], msg, btn)
    else:
        await Message.reply_msg(update, "Use <code>/movie movie_name</code>\nE.g. <code>/movie animal</code>\nor\n<code>/movie -i tt13751694</code> [IMDB ID]\nor\n<code>/movie bodyguard -y 2011</code>")


async def func_translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type == "private":
        msg = " ".join(context.args)
        tr_reply = update.message.reply_to_message
        if tr_reply:
            if tr_reply.text:
                msg = tr_reply.text
            elif tr_reply.caption:
                msg = tr_reply.caption

        if msg != "":
            find_user = MongoDB.find_one("users", "user_id", user.id)
            lang_code = find_user.get("lang")
            try:
                tr_msg = translate(msg, lang_code)
            except Exception as e:
                print(f"Error Translator: {e}")

                lang_code_list = MongoDB.get_data("ciri_docs", "lang_code_list")
                btn = [
                    [InlineKeyboardButton("Language Code List 📃", lang_code_list)]
                ]
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
                return
            
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg)
            else:
                await Message.reply_msg(update, "Something Went Wrong!")
        else:
            await Message.reply_msg(update, "Use <code>/tr text</code> or reply the text with <code>/tr</code>\nE.g. <code>/tr the text you want to translate</code>")

    else:
        await Message.reply_msg(update, "Coming Soon...")


async def func_setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)
    if chat.type == "private":
        if msg != "":
            try:
                MongoDB.update_db("users", "user_id", user.id, "lang", msg)
                await Message.reply_msg(update, f"Language Updated to <code>{msg}</code>. Now you can use /tr command.")
            except Exception as e:
                print(f"Error setting lang code: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        else:
            lang_code_list = MongoDB.get_data("ciri_docs", "lang_code_list")
            btn = [
                [InlineKeyboardButton("Language Code List 📃", lang_code_list)]
            ]
            await Message.send_msg(chat.id, "<code>lang_code</code> can't be leave empty! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
    else:
        await Message.reply_msg(update, "Coming Soon...")


async def func_b64decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if msg != "":
        decode = decode_b64(msg)
        await Message.reply_msg(update, f"Decode: <code>{decode}</code>")
    else:
        await Message.reply_msg(update, "Use <code>/decode text</code>\nE.g. <code>/decode the text you want to decode</code>")


async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if msg != "":
        encode = encode_b64(msg)
        await Message.reply_msg(update, f"Encode: <code>{encode}</code>")
    else:
        await Message.reply_msg(update, "Use <code>/encode text</code>\nE.g. <code>/encode the text you want to encode</code>")


async def func_shortener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if msg != "":
        shorted_url = shortener_url(msg)
        if shorted_url:
            await Message.reply_msg(update, shorted_url)
        else:
            await Message.reply_msg(update, "Something Went Wrong!")
    else:
        await Message.reply_msg(update, "Use <code>/shortener url</code>\nE.g. <code>/shortener https://google.com</code>")


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if msg != "":
        sent_msg = await Message.reply_msg(update, f"Pinging {msg}\nPlease wait...")
        ping = ping_url(msg)
        if ping:
            res = ping[2]
            if res == 200:
                site_status = "<b>∞ Site is online 🟢</b>"
            else:
                site_status = "<b>∞ Site is offline/something went wrong 🔴</b>"

            await Message.edit_msg(update, f"<b>∞ URL:</b> {ping[0]}\n<b>∞ Time(ms):</b> <code>{ping[1]}</code>\n<b>∞ Response Code:</b> <code>{ping[2]}</code>\n{site_status}", sent_msg)
    else:
        await Message.reply_msg(update, "Use <code>/ping url</code>\nE.g. <code>/ping https://google.com</code>")


async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if msg != "":
        if msg:
            await Message.reply_msg(update, f"<b>{msg} = <code>{calc(msg):.2f}</code></b>")
    else:
        await Message.reply_msg(update, "Use <code>/calc math</code>\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")


async def func_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if msg == "on":
            MongoDB.update_db("users", "user_id", user.id, "echo", "on")
            find_one = MongoDB.find_one("users", "user_id", user.id)
            verify = find_one.get("echo")
            if verify == "on":
                await Message.reply_msg(update, "Echo enabled in this chat!")
            else:
                await Message.reply_msg(update, "Something Went Wrong!")
        elif msg == "off":
            MongoDB.update_db("users", "user_id", user.id, "echo", "off")
            find_one = MongoDB.find_one("users", "user_id", user.id)
            verify = find_one.get("echo")
            if verify == "off":
                await Message.reply_msg(update, "Echo disabled in this chat!")
            else:
                await Message.reply_msg(update, "Something Went Wrong!")
        elif msg == "":
            await Message.reply_msg(update, "Use <code>/echo on</code> to turn on.\nUse <code>/echo off</code> to turn off.")

    else:
        await Message.reply_msg(update, "Coming Soon...")


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    replied_msg = update.message.reply_to_message

    if user.id == int(owner_id):
        if replied_msg:
            msg = replied_msg.text
        else:
            await Message.reply_msg(update, "Reply a message to broadcast!")
            return
        
        users = MongoDB.find("users", "user_id")
        x = MongoDB.info_db("users")

        sent_count = 0
        notify = await Message.send_msg(owner_id, f"Sent: {sent_count}\nTotal User: {x[1]}")
        for user_id in users:
            try:
                await Message.send_msg(user_id, msg)
                sent_count += 1
                await Message.edit_msg(update, f"Sent: {sent_count}\nTotal User: {x[1]}", notify)
            except Exception as e:
                print(f"Error Broadcast: {e}")
        await Message.reply_msg(update, "Job Done !!")

    else:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Message.reply_msg(update, MessageStorage.help_msg())


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = " ".join(context.args)
    if user.id == int(owner_id):
        if msg != "":
            db = MongoDB.info_db(msg)
            if db:
                msg = (
                    f"▬▬▬▬▬▬▬▬▬▬\n"
                    f"Doc Name:<code> {db[0]}</code>\n"
                    f"Doc Count:<code> {db[1]}</code>\n"
                    f"Doc Size:<code> {db[2]}</code>\n"
                    f"Actual Size:<code> {db[3]}</code>\n"
                    f"▬▬▬▬▬▬▬▬▬▬\n"
                )
        else:
            db = MongoDB.info_db()
            msg = "▬▬▬▬▬▬▬▬▬▬\n"
            for info in db:
                msg += (
                    f"Doc Name:<code> {info[0]}</code>\n"
                    f"Doc Count:<code> {info[1]}</code>\n"
                    f"Doc Size:<code> {info[2]}</code>\n"
                    f"Actual Size:<code> {info[3]}</code>\n"
                    f"▬▬▬▬▬▬▬▬▬▬\n"
                )

        await Message.reply_msg(update, f"<b>{msg}</b>")

    else:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.message.text

    if chat.type == "private":
        find_user = MongoDB.find_one("users", "user_id", user.id)
        echo_status = find_user.get("echo")
        if echo_status == "on":
            await Message.reply_msg(update, msg)


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", func_start))
    application.add_handler(CommandHandler("movie", func_movieinfo))
    application.add_handler(CommandHandler("tr", func_translator))
    application.add_handler(CommandHandler("setlang", func_setlang))
    application.add_handler(CommandHandler("decode", func_b64decode))
    application.add_handler(CommandHandler("encode", func_b64encode))
    application.add_handler(CommandHandler("shortener", func_shortener))
    application.add_handler(CommandHandler("ping", func_ping))
    application.add_handler(CommandHandler("calc", func_calc))
    application.add_handler(CommandHandler("echo", func_echo))
    application.add_handler(CommandHandler("help", func_help))
    # owner
    application.add_handler(CommandHandler("broadcast", func_broadcast))
    application.add_handler(CommandHandler("database", func_database))
    # filters
    application.add_handler(MessageHandler(filters.ALL, func_filter_all))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("🤖 Bot Started !!")
    main()
