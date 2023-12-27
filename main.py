import asyncio
from telegram import Update, InlineKeyboardButton, ChatMember
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

    else:
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


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    get_bot = await bot.get_me()
    get_bot_permission = await chat.get_member(get_bot.id)
    get_user_permission = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if get_user_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            if get_bot_permission.status == ChatMember.ADMINISTRATOR:
                try:
                    if reply:
                        get_user_permission = await chat.get_member(reply.from_user.id)
                        if get_user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            await bot.ban_chat_member(chat.id, reply.from_user.id)
                            await Message.reply_msg(update, f"{user.mention_html()} has been banned!")
                        elif get_bot.id == reply.from_user.id:
                            await Message.reply_msg(update, "Really? Should I leave? 😐")
                        else:
                            await Message.reply_msg(update, "I'm not going to ban an admin!")
                    else:
                        await Message.reply_msg(update, "Reply the user message with command to ban him/her!")
                except Exception as e:
                    print(f"Error user ban: {e}")
            else:
                await Message.reply_msg(update, "I'm not an admin in this chat!")
        else:
            await Message.reply_msg(update, "You aren't an admin of this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]

        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    get_bot = await bot.get_me()
    get_bot_permission = await chat.get_member(get_bot.id)
    get_user_permission = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if get_user_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            if get_bot_permission.status == ChatMember.ADMINISTRATOR:
                try:
                    if reply:
                        get_user_permission = await chat.get_member(reply.from_user.id)
                        if get_user_permission.status == ChatMember.BANNED:
                            await bot.unban_chat_member(chat.id, reply.from_user.id)
                            await Message.reply_msg(update, f"{user.mention_html()} has been unbanned! He/She can join again!")
                        elif get_bot.id == reply.from_user.id:
                            await Message.reply_msg(update, "What is happening here? Why should I ban or unban myslef? Should I leave? 😐")
                        else:
                            await Message.reply_msg(update, "Wrong command for this task!")
                    else:
                        await Message.reply_msg(update, "Reply the user message with command to unban him/her!")
                except Exception as e:
                    print(f"Error user unban: {e}")
            else:
                await Message.reply_msg(update, "I'm not an admin in this chat!")
        else:
            await Message.reply_msg(update, "You aren't an admin of this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]

        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)



async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    get_bot = await bot.get_me()
    get_bot_permission = await chat.get_member(get_bot.id)
    get_user_permission = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if get_user_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            if get_bot_permission.status == ChatMember.ADMINISTRATOR:
                try:
                    if reply:
                        get_user_permission = await chat.get_member(reply.from_user.id)
                        if get_user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            await bot.ban_chat_member(chat.id, reply.from_user.id)
                            await bot.unban_chat_member(chat.id, reply.from_user.id)
                            await Message.reply_msg(update, f"{user.mention_html()} has been kicked!")
                        elif get_bot.id == reply.from_user.id:
                            await Message.reply_msg(update, "What is happening here? Why should I kick myslef? Should I leave? 😐")
                        else:
                            await Message.reply_msg(update, "I'm not going to kick an admin!")
                    else:
                        await Message.reply_msg(update, "Reply the user message with command to kick him/her!")         
                except Exception as e:
                    print(f"Error user kick: {e}")
            else:
                await Message.reply_msg(update, "I'm not an admin in this chat!")
        else:
            await Message.reply_msg(update, "You aren't an admin of this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]

        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    get_bot = await bot.get_me()
    get_bot_permission = await chat.get_member(get_bot.id)
    get_user_permission = await chat.get_member(user.id)

    permissions = {
        "can_send_other_messages": False,
        "can_invite_users": False,
        "can_send_polls": False,
        "can_send_messages": False,
        "can_change_info": False,
        "can_pin_messages": False,
        "can_add_web_page_previews": False,
        "can_manage_topics": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_send_video_notes": False,
        "can_send_voice_notes": False
    }

    if chat.type in ["group", "supergroup"]:
        if get_user_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            if get_bot_permission.status == ChatMember.ADMINISTRATOR:
                try:
                    if reply:
                        get_user_permission = await chat.get_member(reply.from_user.id)
                        if get_user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            await bot.restrict_chat_member(chat.id, reply.from_user.id, permissions)
                            await Message.reply_msg(update, f"{user.mention_html()} has been muted 🤫!")
                        elif get_bot.id == reply.from_user.id:
                            await Message.reply_msg(update, "What is happening here? Why you want to mute me? 😐")
                        else:
                            await Message.reply_msg(update, "I'm not going to mute an admin!")
                    else:
                        await Message.reply_msg(update, "Reply the user message with command to mute him/her!")         
                except Exception as e:
                    print(f"Error user mute: {e}")
            else:
                await Message.reply_msg(update, "I'm not an admin in this chat!")
        else:
            await Message.reply_msg(update, "You aren't an admin of this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]

        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    get_bot = await bot.get_me()
    get_bot_permission = await chat.get_member(get_bot.id)
    get_user_permission = await chat.get_member(user.id)

    permissions = {
        "can_send_other_messages": True,
        "can_invite_users": True,
        "can_send_polls": True,
        "can_send_messages": True,
        "can_change_info": True,
        "can_pin_messages": True,
        "can_add_web_page_previews": True,
        "can_manage_topics": True,
        "can_send_audios": True,
        "can_send_documents": True,
        "can_send_photos": True,
        "can_send_videos": True,
        "can_send_video_notes": True,
        "can_send_voice_notes": True
    }

    if chat.type in ["group", "supergroup"]:
        if get_user_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            if get_bot_permission.status == ChatMember.ADMINISTRATOR:
                try:
                    if reply:
                        get_user_permission = await chat.get_member(reply.from_user.id)
                        if get_user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            await bot.restrict_chat_member(chat.id, reply.from_user.id, permissions)
                            await Message.reply_msg(update, f"{user.mention_html()} has been unmuted 😉! You can speak again {user.mention_html()}!")
                        elif get_bot.id == reply.from_user.id:
                            await Message.reply_msg(update, "Wrong command for this task!")
                        else:
                            await Message.reply_msg(update, "Wrong command for this task!")
                    else:
                        await Message.reply_msg(update, "Reply the user message with command to unmute him/her!")         
                except Exception as e:
                    print(f"Error user mute: {e}")
            else:
                await Message.reply_msg(update, "I'm not an admin in this chat!")
        else:
            await Message.reply_msg(update, "You aren't an admin of this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]

        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Message.reply_msg(update, MessageStorage.help_msg())


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
    application.add_handler(CommandHandler("ban", func_ban))
    application.add_handler(CommandHandler("unban", func_unban))
    application.add_handler(CommandHandler("kick", func_kick))
    application.add_handler(CommandHandler("mute", func_mute))
    application.add_handler(CommandHandler("unmute", func_unmute))
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
