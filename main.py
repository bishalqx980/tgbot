import asyncio
import time
import datetime
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, ChatMember
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot import bot_token, bot, owner_id, owner_username, server_url, chatgpt_usage_limit, chatgpt_usage_reset_time
from bot.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.ping import ping_url
from bot.shortener import shortener_url
from bot.translator import translate
from bot.base64 import decode_b64, encode_b64
from bot.omdb_movie_info import get_movie_info
from bot.utils import calc
from bot.helper.tgmsg_storage import MessageStorage
from bot.safone import Safone
from bot.group_management import func_ban, func_unban, func_kick, func_mute, func_unmute, func_adminlist


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    bot_info = await bot.get_me()
    avatar = MongoDB.get_data("ciri_docs", "avatar")

    if chat.type == "private":
        welcome_msg = MessageStorage.welcome_msg()
        welcome_msg = welcome_msg[0].format(
            user_mention = user.mention_html(),
            bot_username = bot_info.username,
            bot_firstname = bot_info.first_name
        )

        btn = [
            [
                InlineKeyboardButton("Add in Group", f"http://t.me/{bot_info.username}?startgroup=start"),
                InlineKeyboardButton("⚡ Developer ⚡", f"https://t.me/{owner_username}")
            ]
        ]
        await Message.send_img(chat.id, avatar, welcome_msg, btn)

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

    elif chat.type in ["group", "supergroup"]:
        chat = update.effective_chat
        find_db = MongoDB.find_one("groups", "chat_id", chat.id)

        if not find_db:
            data = {
                "chat_id": chat.id,
                "Title": chat.title
            }
            MongoDB.insert_single_data("groups", data)

        welcome_msg = MessageStorage.welcome_msg()
        welcome_msg = welcome_msg[1].format(
            user_mention = user.mention_html()
        )

        btn = [
            [
                InlineKeyboardButton("Start me in private", f"http://t.me/{bot_info.username}?start=start")
            ]
        ]
        await Message.send_msg(chat.id, welcome_msg, btn)


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
        find_user = MongoDB.find_one("users", "user_id", user.id)
        lang_code = find_user.get("lang")
    elif chat.type in ["group", "supergroup"]:
        find_group = MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            lang_code = find_group.get("lang")
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...")
            return

    msg = " ".join(context.args)
    tr_reply = update.message.reply_to_message
    if tr_reply:
        if tr_reply.text:
            msg = tr_reply.text
        elif tr_reply.caption:
            msg = tr_reply.caption

    if msg != "":
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
            await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)
        else:
            await Message.reply_msg(update, "Something Went Wrong!")
    else:
        await Message.reply_msg(update, "Use <code>/tr text</code> or reply the text with <code>/tr</code>\nE.g. <code>/tr the text you want to translate</code>")    


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
    elif chat.type in ["group", "supergroup"]:
        get_bot = await bot.get_me()
        getper_bot = await chat.get_member(get_bot.id)
        getper_user = await chat.get_member(user.id)

        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                if msg != "":
                    try:
                        get_chat = MongoDB.find_one("groups", "chat_id", chat.id)
                        if get_chat:
                            MongoDB.update_db("groups", "chat_id", chat.id, "lang", msg)
                            await Message.reply_msg(update, f"Language Updated to <code>{msg}</code>. Now you can use /tr command.")
                        else:
                            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
                            return
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
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")


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
        if msg[0:4] != "http":
            msg = f"http://{msg}"

        sent_msg = await Message.reply_msg(update, f"Pinging {msg}\nPlease wait...")
        ping = ping_url(msg)

        if ping:
            res = ping[2]
            if res == 200:
                site_status = "<b>∞ Site is online 🟢</b>"
            else:
                site_status = "<b>∞ Site is offline/something went wrong 🔴</b>"
              
            btn = [
                [
                    InlineKeyboardButton("Visit Site", f"{ping[0]}")
                ]
            ]

            await Message.edit_msg(update, f"<b>∞ URL:</b> {ping[0]}\n<b>∞ Time(ms):</b> <code>{ping[1]}</code>\n<b>∞ Response Code:</b> <code>{ping[2]}</code>\n{site_status}", sent_msg, btn)
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


async def func_webshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    url = " ".join(context.args)
    if url:
        sent_msg = await Message.reply_msg(update, "Generating please wait...")
        webshot = await Safone.webshot(url)
        if webshot:
            try:
                await Message.del_msg(chat.id, sent_msg)
                await Message.send_img(chat.id, webshot, f"✨ {url}")
            except Exception as e:
                await Message.reply_msg(update, f"Error: {e}")
        else:
            await Message.reply_msg(update, "Something Went Wrong!")
    else:
        await Message.reply_msg(update, "Use <code>/webshot url</code>\nE.g. <code>/webshot https://google.com</code>")


async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if msg == "on":
            MongoDB.update_db("users", "user_id", user.id, "chatgpt", "on")
            find_one = MongoDB.find_one("users", "user_id", user.id)
            verify = find_one.get("chatgpt")
            if verify == "on":
                await Message.reply_msg(update, "ChatGPT AI enabled in this chat!")
            else:
                await Message.reply_msg(update, "Something Went Wrong!")
        elif msg == "off":
            MongoDB.update_db("users", "user_id", user.id, "chatgpt", "off")
            find_one = MongoDB.find_one("users", "user_id", user.id)
            verify = find_one.get("chatgpt")
            if verify == "off":
                await Message.reply_msg(update, "ChatGPT AI disabled in this chat!")
            else:
                await Message.reply_msg(update, "Something Went Wrong!")
        elif msg == "":
            await Message.reply_msg(update, "Use <code>/chatgpt on</code> to turn on.\nUse <code>/chatgpt off</code> to turn off.")
    else:
        await Message.reply_msg(update, "Coming Soon...")


async def func_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if msg:
            user_id = int(msg)
        else:
            user_id = user.id

        find_mongodb = MongoDB.find_one("users", "user_id", user_id)

        if find_mongodb:
            user_mention = find_mongodb.get("mention")
            lang = find_mongodb.get("lang")
            echo = find_mongodb.get("echo")
            chatgpt = find_mongodb.get("chatgpt")
            chatgpt_req_count = find_mongodb.get("chatgpt_req_count")

            text = f"<b>⚜ Data of <code>{user_id}</code></b>\n\n◉ User: {user_mention}\n◉ Lang: <code>{lang}</code>\n◉ Echo: <code>{echo}</code>\n◉ ChatGPT: <code>{chatgpt}</code>\n◉ ChatGPT Req: <code>{chatgpt_req_count}</code>"
            await Message.reply_msg(update, text)
        else:
            await Message.reply_msg(update, "User not found!")
    elif chat.type in ["group", "supergroup"]:
        await Message.reply_msg(update, "Coming Soon...")


async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message

    if chat.type == "private":
        if reply:
            if reply.forward_from:
                from_user_id = reply.forward_from.id
            elif reply.from_user:
                from_user_id = reply.from_user.id

            await Message.reply_msg(update, f"◉ Your UserID: <code>{user.id}</code>\n◉ Replied UserID: <code>{from_user_id}</code>")
        else:
            await Message.reply_msg(update, f"◉ UserID: <code>{user.id}</code>")
    else:
        if reply:
            if reply.forward_from:
                from_user_id = reply.forward_from.id
            elif reply.from_user:
                from_user_id = reply.from_user.id

            await Message.reply_msg(update, f"◉ Your UserID: <code>{user.id}</code>\n◉ Replied UserID: <code>{from_user_id}</code>\n◉ ChatID: <code>{chat.id}</code>")
        else:
            await Message.reply_msg(update, f"◉ UserID: <code>{user.id}</code>\n◉ ChatID: <code>{chat.id}</code>")


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Message.reply_msg(update, MessageStorage.help_msg())


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    replied_msg = update.message.reply_to_message
    user_id = " ".join(context.args)

    if user.id == int(owner_id):
        if replied_msg:
            msg = replied_msg.text
        else:
            await Message.reply_msg(update, "Reply a message to broadcast!")
            return
        
        if user_id:
            try:
                await Message.send_msg(user_id, msg)
                await Message.reply_msg(update, "Job Done !!")
            except Exception as e:
                print(f"Error Broadcast: {e}")
                await Message.reply_msg(update, f"Error Broadcast: {e}")
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


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = " ".join(context.args)
    if user.id == int(owner_id):
        if msg != "":
            db = MongoDB.find_one("users", "user_id", int(msg))
            if db:
                msg = db
            else:
                msg = f"Data not found!"
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

    if chat.type == "private" and msg:
        find_user = MongoDB.find_one("users", "user_id", user.id)
        # status
        echo_status = find_user.get("echo")
        chatgpt_status = find_user.get("chatgpt")

        # Trigger
        if echo_status == "on":
            await Message.reply_msg(update, msg)

        if chatgpt_status == "on":
            chatgpt_premium = MongoDB.get_data("chatgpt", "chatgpt_premium")
            find_user = MongoDB.find_one("users", "user_id", user.id)
            chatgpt_req_count = find_user.get("chatgpt_req_count")
            if chatgpt_req_count == None:
                chatgpt_req_count = 0

            if user.id == int(owner_id):
                g_msg = "✨ Hi Boss, Please wait!! Generating Response..."
            elif user.id in chatgpt_premium:
                g_msg = f"✨ Hi {user.first_name}, Please wait!! Generating Response..."
            else:
                if chatgpt_req_count == int(chatgpt_usage_limit):
                    chatgpt_seller = MongoDB.get_data("chatgpt", "chatgpt_seller")
                    if chatgpt_seller == None:
                        chatgpt_seller = owner_username
                    btn = [
                        [
                            InlineKeyboardButton("Buy Premium ✨", f"https://t.me/{chatgpt_seller}")
                        ]
                    ]
                    await Message.reply_msg(update, f"Your ChatGPT usage limit Exceeded!\nContact @{chatgpt_seller} to buy ChatGPT Premium!\n\n⩙ Usage: {chatgpt_req_count} out of {chatgpt_usage_limit}", btn)
                    return
                else:
                    g_msg = f"✨ Hi {user.first_name}, Please wait!! Generating Response..."
                
            sent_msg = await Message.reply_msg(update, g_msg)

            safone_ai_res = await Safone.safone_ai(msg)
            if safone_ai_res:
                chatgpt = safone_ai_res[0]
                bard = safone_ai_res[1]
                chatbot = safone_ai_res[2]

                if chatgpt:
                    text = chatgpt.message
                elif bard:
                    text = bard.message
                else:
                    text = chatbot.response

                await Message.edit_msg(update, text, sent_msg, parse_mode=ParseMode.MARKDOWN)
                chatgpt_req_count += 1
                MongoDB.update_db("users", "user_id", user.id, "chatgpt_req_count", chatgpt_req_count)
            else:
                await Message.edit_msg(update, "Something Went Wrong!", sent_msg)


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
    application.add_handler(CommandHandler("webshot", func_webshot))
    application.add_handler(CommandHandler("chatgpt", func_chatgpt))
    application.add_handler(CommandHandler("stats", func_stats))
    application.add_handler(CommandHandler("id", func_id))
    application.add_handler(CommandHandler("ban", func_ban))
    application.add_handler(CommandHandler("unban", func_unban))
    application.add_handler(CommandHandler("kick", func_kick))
    application.add_handler(CommandHandler("mute", func_mute))
    application.add_handler(CommandHandler("unmute", func_unmute))
    application.add_handler(CommandHandler("adminlist", func_adminlist))
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
