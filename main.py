import os
import json
import psutil
import asyncio
import requests
import threading
import subprocess
from datetime import datetime
from telegram.constants import ParseMode
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ChatMemberHandler
from bot import logger, bot_token, bot, owner_id, owner_username, bot_pic, lang_code_list, welcome_img, support_chat, telegraph, server_url, chatgpt_limit, usage_reset, ai_imagine_limit
from bot.mongodb import MongoDB
from bot.helper import commands
from bot.helper.telegram_helper import Message, Button
from bot.features.ping import ping_url
from bot.features.shortener import shortener_url
from bot.features.translator import translate
from bot.features.base64 import decode_b64, encode_b64
from bot.features.omdb_movie_info import get_movie_info
from bot.features.utils import calc
from bot.features.safone import Safone
from bot.group_management import func_welcome, func_goodbye, func_antibot, track_chat_activities, func_invite_link, func_pin_msg, func_unpin_msg, func_ban, func_unban, func_kick, func_kickme, func_mute, func_unmute, func_lockchat, func_unlockchat, func_adminlist
from bot.features.ytdl import YouTubeDownload
from bot.helper.callbackbtn_helper import func_callbackbtn
from bot.features.weather import weather_info
from bot.features.g4f import G4F
from bot.features.render import Render


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_msg(update, msg)
        return
    
    if chat.type != "private":
        _bot = await bot.get_me()
        find_db = await MongoDB.find_one("groups", "chat_id", chat.id)

        if not find_db:
            try:
                data = {
                    "chat_id": chat.id,
                    "title": chat.title
                }
                await MongoDB.insert_single_data("groups", data)
                await Message.reply_msg(update, "Group has been registered successfully...")
            except Exception as e:
                logger.error(f"Error registering group: {e}")
                await Message.reply_msg(update, "⚠ Group has not registered, something went wrong...")

        btn_name = ["Start me in private"]
        btn_url = [f"http://t.me/{_bot.username}?start=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, f"Hi, {user.mention_html()}! Start me in private to chat with me 😊!", btn)
        return
    
    _bot = await bot.get_me()
    bot_pic = await MongoDB.get_data("bot_docs", "bot_pic")
    welcome_img = await MongoDB.get_data("bot_docs", "welcome_img")
    support_chat = await MongoDB.get_data("bot_docs", "support_chat")

    msg = (
        f"Hi {user.mention_html()}! I'm <a href='https://t.me/{_bot.username}'>{_bot.first_name}</a>, your all-in-one bot!\n\n"
        f"<blockquote>Here's a short list of what I can do:\n\n" # break
        f"• Get response from <b>ChatGPT AI</b>\n"
        f"• Generate image from your prompt\n"
        f"• Download/Search videos from YouTube\n"
        f"• Provide movie information\n"
        f"• Translate languages\n"
        f"• Encode/decode base64\n"
        f"• Shorten URLs\n"
        f"• Ping any URL\n"
        f"• Be your calculator\n"
        f"• Echo your message for fun\n"
        f"• Take website screenshot\n"
        f"• Provide weather information\n"
        f"• <b>Group management</b>\n"
        f"• & Much more...</blockquote>\n\n"
        f"• /help for bot help\n" # break
        f"<i>More Feature coming soon...</i>\n"
    )

    btn_name_1 = ["Add in Group"]
    btn_url_1 = [f"http://t.me/{_bot.username}?startgroup=start"]
    btn_name_2 = ["⚡ Developer ⚡", "📘 Source Code"]
    btn_url_2 = [f"https://t.me/bishalqx980", "https://github.com/bishalqx980/tgbot"]
    btn_name_3 = ["Support Chat"]
    btn_url_3 = [support_chat]
    btn_1 = await Button.ubutton(btn_name_1, btn_url_1)
    btn_2 = await Button.ubutton(btn_name_2, btn_url_2, True)
    if support_chat:
        btn_3 = await Button.ubutton(btn_name_3, btn_url_3)
        btn = btn_1 + btn_2 + btn_3
    else:
        btn = btn_1 + btn_2

    if welcome_img and bot_pic:
        await Message.send_img(chat.id, bot_pic, msg, btn)
    else:
        await Message.send_msg(chat.id, msg, btn)

    find_db = await MongoDB.find_one("users", "user_id", user.id)
    if not find_db:
        data = {
            "user_id": user.id,
            "Name": user.full_name,
            "username": user.username,
            "mention": user.mention_html(),
            "lang": user.language_code
        }
        try:
            await MongoDB.insert_single_data("users", data)
        except Exception as e:
            logger.error(f"Error registering user: {e}")


async def func_movieinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/movie movie_name</code>\nE.g. <code>/movie animal</code>\nor\n<code>/movie -i tt13751694</code> [IMDB ID]\nor\n<code>/movie bodyguard -y 2011</code>")
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
    elif "-i" and "-y" in msg:
        await Message.reply_msg(update, "⚠ You can't use both statement in same message!\n/movie for details.")

    movie_info = get_movie_info(movie_name=msg, imdb_id=imdb_id, year=year)
    if movie_info:
        msg = (
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
        btn_name = [f"✨ IMDB - {movie_info[2]}"]
        btn_url = [f"https://www.imdb.com/title/{movie_info[16]}"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_img(chat.id, movie_info[0], msg, btn)


async def func_translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if chat.type == "private":
        find_user = await MongoDB.find_one("users", "user_id", user.id)

        if not find_user:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        lang_code = find_user.get("lang")

    elif chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if not find_group:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        lang_code = find_group.get("lang")

    if msg == "auto_on":
        if chat.type == "private":
            try:
                await MongoDB.update_db("users", "user_id", user.id, "auto_tr", "on")
                await Message.reply_msg(update, f"Auto Translator Enabled for this chat!")
            except Exception as e:
                logger.error(f"Error enabling auto tr: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        elif chat.type in ["group", "supergroup"]:
            _bot = await bot.get_me()
            bot_permission = await chat.get_member(_bot.id)
            user_permission = await chat.get_member(user.id)

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.reply_msg(update, "I'm not an admin of this Group!")
                return
            
            if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                await Message.reply_msg(update, "You aren't an admin of this Group!")
                return
            
            try:
                await MongoDB.update_db("groups", "chat_id", chat.id, "auto_tr", "on")
                await Message.reply_msg(update, f"Auto Translator Enabled for this chat!")
            except Exception as e:
                logger.error(f"Error enabling auto tr: {e}")
                await Message.reply_msg(update, f"Error: {e}")

    elif msg == "auto_off":
        if chat.type == "private":
            try:
                await MongoDB.update_db("users", "user_id", user.id, "auto_tr", "off")
                await Message.reply_msg(update, f"Auto Translator Disabled for this chat!")
            except Exception as e:
                logger.error(f"Error disabling auto tr: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        elif chat.type in ["group", "supergroup"]:
            bot_permission = await chat.get_member(_bot.id)
            user_permission = await chat.get_member(user.id)

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.reply_msg(update, "I'm not an admin of this Group!")
                return
            
            if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                await Message.reply_msg(update, "You aren't an admin of this Group!")
                return
            
            try:
                await MongoDB.update_db("groups", "chat_id", chat.id, "auto_tr", "off")
                await Message.reply_msg(update, f"Auto Translator Disabled for this chat!")
            except Exception as e:
                logger.error(f"Error disabling auto tr: {e}")
                await Message.reply_msg(update, f"Error: {e}")

    if not msg:
        await Message.reply_msg(update, "Use <code>/tr text</code> or reply the text with <code>/tr</code>\nE.g. <code>/tr the text you want to translate</code>\n\nAuto translator mode:\nEnable using <code>/tr auto_on</code>\nDisable using <code>/tr auto_off</code>")
        return
    
    try:
        tr_msg = translate(msg, lang_code)
    except Exception as e:
        logger.error(f"Error Translator: {e}")
        lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
        btn_name = ["Language Code List 📃"]
        btn_url = [lang_code_list]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "Chat language not found/invalid! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
        return

    if tr_msg != msg:
        await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await Message.reply_msg(update, "Error: Translated text & main text are same!")


async def func_setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if not msg:
            lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
            btn_name = ["Language Code List 📃"]
            btn_url = [lang_code_list]
            btn = await Button.ubutton(btn_name, btn_url)
            await Message.send_msg(chat.id, "<code>lang_code</code> can't be leave empty! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
            return
        
        try:
            await MongoDB.update_db("users", "user_id", user.id, "lang", msg)
            await Message.reply_msg(update, f"Language Updated to <code>{msg}</code>. Now you can use /tr command.")
        except Exception as e:
            logger.error(f"Error setting lang code: {e}")
            await Message.reply_msg(update, f"Error: {e}")

    elif chat.type in ["group", "supergroup"]:
        _bot = await bot.get_me()
        bot_permission = await chat.get_member(_bot.id)
        user_permission = await chat.get_member(user.id)

        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.reply_msg(update, "I'm not an admin of this Group!")
            return
        
        if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            await Message.reply_msg(update, "You aren't an admin of this Group!")
            return
        
        if not msg:
            lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
            btn_name = ["Language Code List 📃"]
            btn_url = [lang_code_list]
            btn = await Button.ubutton(btn_name, btn_url)
            await Message.send_msg(chat.id, "<code>lang_code</code> can't be leave empty! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
            return
        
        try:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if not find_group:
                await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
                return
            
            await MongoDB.update_db("groups", "chat_id", chat.id, "lang", msg)
            await Message.reply_msg(update, f"Language Updated to <code>{msg}</code>. Now you can use /tr command.")
        except Exception as e:
            logger.error(f"Error setting lang code: {e}")
            await Message.reply_msg(update, f"Error: {e}")           


async def func_b64decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/decode the `Encoded` text</code>\nor reply the `Encoded` text with <code>/decode</code>\nE.g. <code>/decode the `Encoded` text you want to decode</code>")
        return
    
    decode = decode_b64(msg)
    if decode:
        await Message.reply_msg(update, f"<code>{decode}</code>")
    else:
        await Message.reply_msg(update, f"Invalid text!")


async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/encode the `Decoded` or `normal` text</code>\nor reply the `Decoded` or `normal` text with <code>/encode</code>\nE.g. <code>/encode the `Decoded` or `normal` text you want to encode</code>")
        return
    
    encode = encode_b64(msg)
    if encode:
        await Message.reply_msg(update, f"<code>{encode}</code>")
    else:
        await Message.reply_msg(update, f"Invalid text!")


async def func_shortener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/shortener url</code>\nor reply the url with <code>/shortener</code>\nE.g. <code>/shortener https://google.com</code>")
        return
    
    shorted_url = shortener_url(msg)
    if shorted_url:
        await Message.reply_msg(update, shorted_url)
    else:
        await Message.reply_msg(update, f"Invalid URL!")


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)

    if not url:
        await Message.reply_msg(update, "Use <code>/ping url</code>\nE.g. <code>/ping https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_msg(update, f"Pinging {url}\nPlease wait...")
    ping = ping_url(url)

    if ping:
        ping_time, status_code = ping
        if status_code == 200:
            site_status = "<b>∞ Site is online 🟢</b>"
        else:
            site_status = "<b>∞ Site is offline/something went wrong 🔴</b>"
        btn_name = ["Visit Site"]
        btn_url = [url]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.edit_msg(update, f"<b>∞ URL:</b> {url}\n<b>∞ Time(ms):</b> <code>{ping_time}</code>\n<b>∞ Response Code:</b> <code>{status_code}</code>\n{site_status}", sent_msg, btn)   


async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/calc math</code>\nor reply the math with <code>/calc</code>\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")
        return
    
    try:
        await Message.reply_msg(update, f"Calculation result: <code>{calc(msg):.2f}</code>")
    except Exception as e:
        logger.info(f"Can't calc: {e}")
        await Message.reply_msg(update, f"Can't calc: {e}")


async def func_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if msg == "on":
            try:
                await MongoDB.update_db("users", "user_id", user.id, "echo", "on")
                await Message.reply_msg(update, "Echo enabled in this chat!")
            except Exception as e:
                logger.error(f"Error enabling echo: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        elif msg == "off":
            try:
                await MongoDB.update_db("users", "user_id", user.id, "echo", "off")
                await Message.reply_msg(update, "Echo has been disabled in this chat!")
            except Exception as e:
                logger.error(f"Error disabling echo: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        else:
            await Message.reply_msg(update, "Use <code>/echo on</code> to turn on.\nUse <code>/echo off</code> to turn off.")
    elif chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if not find_group:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        _bot = await bot.get_me()
        bot_permission = await chat.get_member(_bot.id)
        user_permission = await chat.get_member(user.id)

        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.reply_msg(update, "I'm not an admin of this Group!")
            return
        
        if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            await Message.reply_msg(update, "You aren't an admin of this Group!")
            return
        
        if msg == "on":
            try:
                await MongoDB.update_db("groups", "chat_id", chat.id, "echo", "on")
                await Message.reply_msg(update, "Echo has been enabled in this chat!")
            except Exception as e:
                logger.error(f"Error enabling echo: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        elif msg == "off":
            try:
                await MongoDB.update_db("groups", "chat_id", chat.id, "echo", "off")
                await Message.reply_msg(update, "Echo disabled in this chat!")
            except Exception as e:
                logger.error(f"Error disabling echo: {e}")
                await Message.reply_msg(update, f"Error: {e}")
        else:
            await Message.reply_msg(update, "Use <code>/echo on</code> to turn on.\nUse <code>/echo off</code> to turn off.")         


async def func_webshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    url = " ".join(context.args)

    if not url:
        await Message.reply_msg(update, "Use <code>/webshot url</code>\nE.g. <code>/webshot https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_msg(update, "Taking webshot please wait...")
    try:
        webshot = await Safone.webshot(url)
        await Message.del_msg(chat.id, sent_msg)
        await Message.send_img(chat.id, webshot, f"✨ {url}")
    except Exception as e:
        logger.error(f"Error taking webshot: {e}")
        await Message.reply_msg(update, f"Error: {e}")      


async def func_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args)

    if not location:
        await Message.reply_msg(update, "Use <code>/weather location_name</code>\nE.g. <code>/weather london</code>")
        return
    
    info = weather_info(location)

    if not info:
        await Message.reply_msg(update, "Something went wrong!")
        return
    
    loc_name = info[0]
    country = info[1]
    zone = info[2]
    localtime = info[3]
    lastupdate = info[4] # last weather update time
    temp_c = info[5]
    f_temp_c = info[6]
    temp_f = info[7]
    f_temp_f = info[8]
    wind_mph = info[9]
    wind_kph = info[10]
    wind_deg = info[11]
    humidity = info[12]
    uv = info[13]
    condition = info[14]
    condition_icon = info[15]
    msg = (
        f"<b>|———LOCATION INFO———|</b>\n\n"
        f"City: <code>{loc_name}</code>\n"
        f"Country: <code>{country}</code>\n"
        f"Zone: <code>{zone}</code>\n"
        f"Local Time: <code>{localtime}</code>\n\n"
        f"<b>|———WEATHER INFO———|</b>\n\n"
        f"➠ {condition} ✨\n\n"
        f"<b>➲ Temperature info</b>\n"
        f"temp (C) » <code>{temp_c}</code>\nFeels » <code>{f_temp_c}</code>\n"
        f"temp (F) » <code>{temp_f}</code>\nFeels » <code>{f_temp_f}</code>\n"
        f"Humidity: <code>{humidity}</code>\n\n"
        f"Wind: <code>{wind_mph}</code> | <code>{wind_kph}</code>\n"
        f"Wind `Angle`: <code>{wind_deg}</code>\n"
        f"UV Ray: <code>{uv}</code>\n\n<pre>⚠ 8 or higher is harmful for skin!</pre>"
    )
    await Message.reply_msg(update, msg)     


async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine a cute cat</code>")
        return
    
    find_user = await MongoDB.find_one("users", "user_id", user.id)

    if not find_user:
        if chat.type == "private":
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        else:
            _bot = await bot.get_me()
            btn_name = ["Start me in private"]
            btn_url = [f"http://t.me/{_bot.username}?start=start"]
            btn = await Button.ubutton(btn_name, btn_url)
            await Message.reply_msg(update, f"User isn't registered!\nStart me in private then try again here!", btn)
            return
        
    ai_imagine_req, last_used = find_user.get("ai_imagine_req"), find_user.get("last_used")
    current_time = datetime.now()

    if not ai_imagine_req:
        ai_imagine_req = 0

    if last_used:
        find = await MongoDB.find("bot_docs", "_id")

        if not find:
            await Message.reply_msg(update, "Something went wrong!")
            return
        
        data = await MongoDB.find_one("bot_docs", "_id", find[0])
        usage_reset, ai_imagine_limit = data.get("usage_reset"), data.get("ai_imagine_limit")

        calc_req = (current_time.timestamp() - last_used.timestamp()) >= int(usage_reset)*3600

        if calc_req:
            ai_imagine_req = 0
            await MongoDB.update_db("users", "user_id", user.id, "ai_imagine_req", ai_imagine_req)
        elif ai_imagine_req >= ai_imagine_limit:
            if user.id != int(owner_id):
                premium_users = data.get("premium_users")
                if not premium_users:
                    premium_users = []

                if user.id not in premium_users:
                    premium_seller = data.get("premium_seller")

                    if not premium_seller:
                        premium_seller = owner_username

                    msg = (
                        f"❗ Your ChatGPT usage limit Exceeded!\n"
                        f"⩙ Usage: {ai_imagine_req} out of {ai_imagine_limit}\n"
                        f"Wait {usage_reset}hour from your <code>last used</code> to reset usage automatically!\n"
                        f"OR Contact @{premium_seller} to buy Premium Account!"
                    )

                    btn_name = ["Buy Premium ✨"]
                    btn_url = [f"https://t.me/{premium_seller}"]
                    btn = await Button.ubutton(btn_name, btn_url)
                    await Message.send_msg(user.id, msg, btn)
                    if chat.type != "private":
                        await Message.reply_msg(update, "Check bot private message!")
                    return
            
    if user.id == int(owner_id):
        msg = "Please wait Boss!! Generating..."
    else:
        msg = f"Please wait {user.first_name}!! Generating..."
    
    sent_msg = await Message.reply_msg(update, msg)

    """
    imagine = await Safone.imagine(prompt)
    """

    imagine = await G4F.imagine(prompt)

    if not imagine:
        await Message.edit_msg(update, "Something Went Wrong!", sent_msg)
        return
    
    try:
        await Message.del_msg(chat.id, sent_msg)
        await Message.send_img(chat.id, imagine, f"✨ {prompt}")
        ai_imagine_req += 1
        await MongoDB.update_db("users", "user_id", user.id, "ai_imagine_req", ai_imagine_req)
        await MongoDB.update_db("users", "user_id", user.id, "last_used", current_time)
    except Exception as e:
        logger.error(f"Error Imagine: {e}")
        await Message.reply_msg(update, f"Error Imagine: {e}")


async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "Use <code>/chatgpt your_prompt</code>\nE.g. <code>/chatgpt What is AI?</code>")
        return
    
    find_user = await MongoDB.find_one("users", "user_id", user.id)

    if not find_user:
        if chat.type == "private":
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        else:
            _bot = await bot.get_me()
            btn_name = ["Start me in private"]
            btn_url = [f"http://t.me/{_bot.username}?start=start"]
            btn = await Button.ubutton(btn_name, btn_url)
            await Message.reply_msg(update, f"User isn't registered!\nStart me in private then try again here!", btn)
            return
        
    chatgpt_req, last_used = find_user.get("chatgpt_req"), find_user.get("last_used")
    current_time = datetime.now()

    if not chatgpt_req:
        chatgpt_req = 0

    if last_used:
        find = await MongoDB.find("bot_docs", "_id")

        if not find:
            await Message.reply_msg(update, "Something went wrong!")
            return
        
        data = await MongoDB.find_one("bot_docs", "_id", find[0])
        usage_reset, chatgpt_limit = data.get("usage_reset"), data.get("chatgpt_limit")

        calc_req = (current_time.timestamp() - last_used.timestamp()) >= int(usage_reset)*3600

        if calc_req:
            chatgpt_req = 0
            await MongoDB.update_db("users", "user_id", user.id, "chatgpt_req", chatgpt_req)
        elif chatgpt_req >= chatgpt_limit:
            if user.id != int(owner_id):
                premium_users = data.get("premium_users")
                if not premium_users:
                    premium_users = []

                if user.id not in premium_users:
                    premium_seller = data.get("premium_seller")

                    if not premium_seller:
                        premium_seller = owner_username

                    msg = (
                        f"❗ Your ChatGPT usage limit Exceeded!\n"
                        f"⩙ Usage: {chatgpt_req} out of {chatgpt_limit}\n"
                        f"Wait {usage_reset}hour from your <code>last used</code> to reset usage automatically!\n"
                        f"OR Contact @{premium_seller} to buy Premium Account!"
                    )

                    btn_name = ["Buy Premium ✨"]
                    btn_url = [f"https://t.me/{premium_seller}"]
                    btn = await Button.ubutton(btn_name, btn_url)
                    await Message.send_msg(user.id, msg, btn)
                    if chat.type != "private":
                        await Message.reply_msg(update, "Check bot private message!")
                    return
            
    if user.id == int(owner_id):
        msg = "Please wait Boss!! Thinking..."
    else:
        msg = f"Please wait {user.first_name}!! Thinking..."
    
    sent_msg = await Message.reply_msg(update, msg)

    """
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
    """

    g4f_gpt = await G4F.chatgpt(prompt)

    if not g4f_gpt:
        await Message.edit_msg(update, "Something Went Wrong!", sent_msg)
        return
    
    try:
        await Message.edit_msg(update, g4f_gpt, sent_msg, parse_mode=ParseMode.MARKDOWN)
        chatgpt_req += 1
        await MongoDB.update_db("users", "user_id", user.id, "chatgpt_req", chatgpt_req)
        await MongoDB.update_db("users", "user_id", user.id, "last_used", current_time)
    except Exception as e:
        logger.error(f"Error ChatGPT: {e}")
        await Message.edit_msg(update, f"Error ChatGPT: {e}", sent_msg, parse_mode=ParseMode.MARKDOWN)


async def func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    url = re_msg.text if re_msg else " ".join(context.args)
        
    context.user_data["url"] = url
    context.user_data["msg_id"] = e_msg.id
    if chat.type != "private":
        _bot = await bot.get_me()
        btn_name = ["Start me in private"]
        btn_url = [f"http://t.me/{_bot.username}?start=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.reply_msg(update, f"Coming Soon...\nYou can use this feature in bot private chat!", btn)
        return
    
    if not url:
        await Message.reply_msg(update, "Use <code>/ytdl youtube_url</code> to download a video!")
        return
    
    btn_name = ["mp4", "mp3"]
    btn_close = ["close"]
    btn = await Button.cbutton(btn_name, btn_name, True)
    btn2 = await Button.cbutton(btn_close, btn_close)
    await Message.reply_msg(update, f"Select Content Quality/Format\n{url}", btn + btn2)


async def exe_func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE, url, extention):
    chat = update.effective_chat

    tmp_msg = await Message.send_msg(chat.id, "Please Wait...")
    await Message.edit_msg(update, "📥 Downloading...", tmp_msg)

    res = await YouTubeDownload.ytdl(url, extention)

    if not res:
        await Message.edit_msg(update, "Something Went Wrong...", tmp_msg)
        return
    
    await Message.edit_msg(update, "📤 Uploading...", tmp_msg)
    try_attempt, max_attempt = 0, 3
    msg_id = context.user_data.get("msg_id")
    while try_attempt <= max_attempt:
        try:
            if extention == "mp4":
                title = res[0]
                file_path = res[1]
                thumbnail = res[2]
                await Message.send_vid(chat.id, file_path, thumbnail, title, msg_id)
                break
            elif extention == "mp3":
                title = res[0]
                file_path = res[1]
                await Message.send_audio(chat.id, file_path, title, title, msg_id)
                break
        except Exception as e:
            logger.error(f"Error Uploading: {e}")
            try_attempt += 1
            await Message.edit_msg(update, f"📤 Uploading... [Retry Attempt: {try_attempt}/{max_attempt}]", tmp_msg)
            if try_attempt == max_attempt:
                logger.error(f"Error Uploading: {e}")
                await Message.send_msg(chat.id, f"Error Uploading: {e}")
                break
            logger.info(f"Waiting {2**try_attempt}sec before retry...")
            await asyncio.sleep(2**try_attempt)
    try:
        if len(res) >= 3:
            removeable_files = [res[1], res[2]]
        else:
            removeable_files = [res[1]]
        for rem in removeable_files:
            os.remove(rem)
        logger.info("Files Removed...")
        await Message.del_msg(chat.id, tmp_msg)
    except Exception as e:
        logger.error(f"Error os.remove: {e}")  


async def func_yts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = " ".join(context.args)

    if not keyword:
        await Message.reply_msg(update, "Use <code>/yts keyword</code>\nE.g. <code>/yts google keynote</code>")
        return
    
    result = await YouTubeDownload.yts(keyword)
    if not result:
        await Message.reply_msg(update, "Something Went Wrong...")  
        return
    
    urls = [
        result[0].watch_url,
        result[1].watch_url,
        result[2].watch_url
    ]
    for url in urls:
        await Message.reply_msg(update, url, disable_web_preview=False)
    await Message.reply_msg(update, f"Video found: {len(result)}\nShowing top {len(urls)} videos!\nTo download videos you can use /ytdl")         


async def func_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if chat.type == "private":
        if msg:
            if user.id != int(owner_id):
                await Message.reply_msg(update, f"Access Denied! [owner only]")
                return
            else:
                chat_id = int(msg)
        else:
            chat_id = user.id

        find_user = await MongoDB.find_one("users", "user_id", chat_id)

        if not find_user:
            find_group = await MongoDB.find_one("groups", "chat_id", chat_id)

        if find_user:
            user_mention = find_user.get("mention")
            lang = find_user.get("lang")
            echo = find_user.get("echo")
            auto_tr = find_user.get("auto_tr")
            chatgpt = find_user.get("chatgpt")
            chatgpt_req = find_user.get("chatgpt_req")
            ai_imagine_req = find_user.get("ai_imagine_req")
            last_used = find_user.get("last_used")
            is_premium = "False"

            find = await MongoDB.find("bot_docs", "_id")
            if find:
                data = await MongoDB.find_one("bot_docs", "_id", find[0])
                premium_users = data.get("premium_users")
                if premium_users:
                    if chat_id in premium_users:
                        is_premium = "True"

            text = (
                f"<b>Data of <code>{chat_id}</code></b>\n"
                f"▬▬▬▬▬▬▬▬▬▬\n"
                f"• User: {user_mention}\n"
                f"• Lang: <code>{lang}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n"
                f"• ChatGPT: <code>{chatgpt}</code>\n"
                f"• ChatGPT Req: <code>{chatgpt_req}/{chatgpt_limit}</code>\n"
                f"• AI Imagine Req: <code>{ai_imagine_req}/{ai_imagine_limit}</code>\n"
                f"• Last Used: <code>{last_used}</code>\n"
                f"• Premium user: <code>{is_premium}</code>\n"
            )
            await Message.reply_msg(update, text)
        elif find_group:
            title = find_group.get("title")
            lang = find_group.get("lang")
            echo = find_group.get("echo")
            auto_tr = find_group.get("auto_tr")
            welcome_msg = find_group.get("welcome_msg")
            goodbye_msg = find_group.get("goodbye_msg")
            antibot = find_group.get("antibot")

            text = (
                f"<b>Data of <code>{chat_id}</code></b>\n"
                f"▬▬▬▬▬▬▬▬▬▬\n"
                f"• Title: {title}\n"
                f"• Lang: <code>{lang}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n"
                f"• Welcome msg: <code>{welcome_msg}</code>\n"
                f"• Goodbye msg: <code>{goodbye_msg}</code>\n"
                f"• Antibot: <code>{antibot}</code>\n"
            )
            await Message.reply_msg(update, text)
        else:
            await Message.reply_msg(update, "User/Chat not found!")
    elif chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if not find_group:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        title = find_group.get("title")
        lang = find_group.get("lang")
        echo = find_group.get("echo")
        auto_tr = find_group.get("auto_tr")
        welcome_msg = find_group.get("welcome_msg")
        goodbye_msg = find_group.get("goodbye_msg")
        antibot = find_group.get("antibot")

        text = (
            f"<b>Data of <code>{chat.id}</code></b>\n"
            f"▬▬▬▬▬▬▬▬▬▬\n"
            f"• Title: {title}\n"
            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Welcome msg: <code>{welcome_msg}</code>\n"
            f"• Goodbye msg: <code>{goodbye_msg}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
        )
        await Message.reply_msg(update, text)          


async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message

    if re_msg:
        if re_msg.forward_from:
            from_user_id = re_msg.forward_from.id
        elif re_msg.from_user:
            from_user_id = re_msg.from_user.id

    if chat.type == "private" and re_msg:
        await Message.reply_msg(update, f"• Your UserID: <code>{user.id}</code>\n• Replied UserID: <code>{from_user_id}</code>")
    elif chat.type == "private":
        await Message.reply_msg(update, f"• UserID: <code>{user.id}</code>")
    elif chat.type in ["group", "supergroup"] and re_msg:
        await Message.reply_msg(update, f"• Your UserID: <code>{user.id}</code>\n• Replied UserID: <code>{from_user_id}</code>\n• ChatID: <code>{chat.id}</code>")
    elif chat.type in ["group", "supergroup"]:
        await Message.reply_msg(update, f"• UserID: <code>{user.id}</code>\n• ChatID: <code>{chat.id}</code>")


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        _bot = await bot.get_me()
        btn_name = ["Start me in private"]
        btn_url = [f"http://t.me/{_bot.username}?start=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.reply_msg(update, f"Hi, {user.mention_html()}! Start me in private to chat with me 😊!", btn)
        return

    message = "<b>Available Bot Command's</b>\n\n"
    for cmd in commands:
        message += (f"/{cmd.command} » <i>{cmd.description}</i>\n")
    
    await Message.reply_msg(update, message)


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    replied_msg = update.message.reply_to_message
    user_id = " ".join(context.args)

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    msg = replied_msg.text or replied_msg.caption if replied_msg else None

    if not msg:
        await Message.reply_msg(update, "Reply a message to broadcast!")
        return
    
    if user_id:
        try:
            if replied_msg.text:
                await Message.send_msg(user_id, msg)
            elif replied_msg.caption:
                await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)
            await Message.reply_msg(update, "Job Done !!")
        except Exception as e:
            logger.error(f"Error Broadcast: {e}")
            await Message.reply_msg(update, f"Error Broadcast: {e}")
        return
    
    users_id = await MongoDB.find("users", "user_id")

    sent_count, except_count = 0, 0
    notify = await Message.send_msg(owner_id, f"Total User: {len(users_id)}")
    for user_id in users_id:
        try:
            if replied_msg.text:
                await Message.send_msg(user_id, msg)
            elif replied_msg.caption:
                await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)     
            sent_count += 1
            progress = (sent_count+except_count)*100/len(users_id)
            await Message.edit_msg(update, f"Total User: {len(users_id)}\nSent: {sent_count}\nBlocked/Deleted: {except_count}\nProgress: {int(progress)}%", notify)
        except Exception as e:
            except_count += 1
            logger.error(f"Error Broadcast: {e}")
    await Message.reply_msg(update, "Job Done !!")


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    msg = " ".join(context.args)

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    db = await MongoDB.info_db()
    msg = "▬▬▬▬▬▬▬▬▬▬\n"
    for info in db:
        msg += (
            f"<code>Doc name   :</code> {info[0]}\n"
            f"<code>Doc count  :</code> {info[1]}\n"
            f"<code>Doc size   :</code> {info[2]}\n"
            f"<code>Actual size:</code> {info[3]}\n"
            f"▬▬▬▬▬▬▬▬▬▬\n"
        )
    await Message.reply_msg(update, f"<b>{msg}</b>")


async def func_cleardb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    c_name = "bot_docs"

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    try:
        await MongoDB.delete_all_doc(c_name)
        data = {
            "bot_pic": bot_pic,
            "telegraph": telegraph,
            "support_chat": support_chat,
            "lang_code_list": lang_code_list,
            "welcome_img": bool(welcome_img),
            "server_url": server_url,
            "chatgpt_limit": chatgpt_limit,
            "ai_imagine_limit": ai_imagine_limit,
            "usage_reset": usage_reset
        }
        await MongoDB.insert_single_data(c_name, data)
        await Message.reply_msg(update, "Database cleaned up! And restored with <code>config.env</code> file entry's!")
    except Exception as e:
        error = f"Error cleardb: {e}"
        await Message.reply_msg(update, error)
        logger.error(error)


async def func_bsetting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    key = " ".join(context.args)
    c_name = "bot_docs"

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if not key:
        find = await MongoDB.find(c_name, "_id")
        if find:
            data = await MongoDB.find_one(c_name, "_id", find[0])
        else:
            data = {
                    "bot_pic": bot_pic,
                    "telegraph": telegraph,
                    "support_chat": support_chat,
                    "lang_code_list": lang_code_list,
                    "welcome_img": bool(welcome_img),
                    "server_url": server_url,
                    "chatgpt_limit": chatgpt_limit,
                    "ai_imagine_limit": ai_imagine_limit,
                    "usage_reset": usage_reset
                }
            await MongoDB.insert_single_data(c_name, data)

            find = await MongoDB.find(c_name, "_id")
            if find:
                data = await MongoDB.find_one(c_name, "_id", find[0])
            else:
                await Message.reply_msg(update, f"Error bsetting: {e}")

        b_pic = data.get("bot_pic")
        tele_graph = data.get("telegraph")
        s_chat = data.get("support_chat")
        lcl = data.get("lang_code_list")
        wel_img = data.get("welcome_img")
        ser_url = data.get("server_url")
        cgpt_l = data.get("chatgpt_limit")
        imagine_l = data.get("ai_imagine_limit")
        u_reset = data.get("usage_reset")
        premium_seller = data.get("premium_seller")
        if not premium_seller:
            premium_seller = f"{owner_username}"
        premium_users = data.get("premium_users")
        if not premium_users:
            premium_users = []
        premium_users_count = len(premium_users) if premium_users else 0

        msg = (
            f"<b>Bot Setting</b>\n"
            f"[collection_name: value]\n\n"
            f"<code>bot_pic          </code>: <i>{b_pic}</i>\n"
            f"<code>telegraph        </code>: <i>{tele_graph}</i>\n"
            f"<code>support_chat     </code>: <i>{s_chat}</i>\n"
            f"<code>lang_code_list   </code>: <i>{lcl}</i>\n"
            f"<code>welcome_img      </code>: <i>{wel_img}</i>\n"
            f"<code>server_url       </code>: <i>{ser_url}</i>\n"
            f"<code>chatgpt_limit    </code>: <i>{cgpt_l}</i>\n"
            f"<code>ai_imagine_limit </code>: <i>{imagine_l}</i>\n"
            f"<code>usage_reset      </code>: <i>{u_reset}</i>\n"
            f"<code>premium_seller    </code>: <i>@{premium_seller}</i>\n"
            f"<code>premium_users     </code>: <i>{premium_users_count} » {premium_users}</i>\n\n"
            f"<i><code>/bsetting collection_name -n new_value</code> (blank new_value means none)</i>\n"
            f"<i>premium_users E.g 12345678, 87654321 ... & premium_seller name without @</i>\n"
            f"<i><code>/cleardb</code> - To clear <code>bot_docs</code> entry's and insert entry from <code>config.env</code> file!</i>"
        )
        await Message.reply_msg(update, f"<b>{msg}</b>")
        return

    if "-n" in key:
        index_n = key.index("-n")
        n_value = key[index_n + len("-n"):].strip()
        if n_value.lower() == "true":
            n_value = bool(True)
        elif n_value.lower() == "false":
            n_value = bool(False)
        key = key[0:index_n].strip()
        if key == "collection_name":
            await Message.reply_msg(update, "⚠ It's an example!!")
            return
    else:
        await Message.reply_msg(update, "<code>-n</code> not provided")
    try:
        o_value = await MongoDB.get_data(c_name, key)
        if key == "premium_users":
            if "," in n_value:
                storage = []
                for user_id in n_value.split(","):
                    storage.append(int(user_id))
                n_value = storage
            else:
                n_value = [int(n_value)]
        await MongoDB.update_db(c_name, key, o_value, key, n_value)
        await Message.reply_msg(update, "Database Updated!")
    except Exception as e:
        logger.error(f"Error bsetting: {e}")
        await Message.reply_msg(update, f"Error bsetting: {e}")     


async def func_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    command = " ".join(context.args)
    command = command.replace("'", "")

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if not command:
        await Message.reply_msg(update, "E.g. <code>/shell dir</code> [linux/windows]\n<code>/shell log</code> to get logger file")
        return
    
    if command == "log":
        with open("log.txt", "rb") as log_file:
            log = log_file.read()
        await Message.send_doc(chat.id, log, "log.txt", "log.txt", e_msg.id)
    else:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            with open('shell.txt', 'w') as shell_file:
                shell_file.write(result.stdout)
            with open("shell.txt", "rb") as shell_file:
                shell = shell_file.read()
            await Message.send_doc(chat.id, shell, "shell.txt", "log.txt", e_msg.id)
        else:
            await Message.reply_msg(update, result.stderr)


async def func_render(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if not msg:
        await Message.reply_msg(update, "E.g. <code>/render list</code>\n<code>/render restart serviceId</code>\n<code>/render redeploy serviceId cache_clear_bool (default True)</code>")
        return
    
    if "list" in msg:
        try:
            res = await Render.list_services()
            msg, null= "", None
            if res:
                res = json.loads(res.text)
            for obj in res:
                service = obj.get("service")
                s_id = service.get("id")
                s_name = service.get("name")
                if s_id:
                    msg += f"<b>{s_name}</b>: <code>{s_id}</code>\n"
            
            await Message.reply_msg(update, msg)
        except Exception as e:
            logger.info(f"Error render: {e}")
            await Message.reply_msg(update, f"Error render: {e}")
    elif "restart" in msg:
        index_restart = msg.index("restart")
        service_id = msg[index_restart + len("restart"):].strip()

        try:
            await Message.reply_msg(update, "Restarting...")
            o_value = await MongoDB.get_data("bot_docs", "bot_status")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "restart")
            await Render.restart(service_id)
        except Exception as e:
            logger.info(f"Error render: {e}")
            await Message.reply_msg(update, f"Error render: {e}")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "alive")
    elif "redeploy" in msg:
        index_redeploy = msg.index("redeploy")
        service_id = msg[index_redeploy + len("redeploy"):].strip()

        try:
            await Message.reply_msg(update, f"Redeploying...")
            o_value = await MongoDB.get_data("bot_docs", "bot_status")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "restart")
            await Render.redeploy(service_id)
        except Exception as e:
            logger.info(f"Error render: {e}")
            await Message.reply_msg(update, f"Error render: {e}")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "alive")


async def func_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != int(owner_id):
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    sys_info = (
        f"<b>↺ System info</b>\n\n"
        f"• CPU\n"
        f"CPU: <code>{psutil.cpu_count()}</code>\n"
        f"CPU (Logical): <code>{psutil.cpu_count(False)}</code>\n"
        f"CPU freq Current: <code>{psutil.cpu_freq()[0]/1024:.2f} Ghz</code>\n"
        f"CPU freq Max: <code>{psutil.cpu_freq()[2]/1024:.2f} Ghz</code>\n\n"
        f"• RAM\n"
        f"RAM Total: <code>{psutil.virtual_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"RAM Avail: <code>{psutil.virtual_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"RAM Used: <code>{psutil.virtual_memory()[3]/(1024**3):.2f} GB</code>\n"
        f"RAM Free: <code>{psutil.virtual_memory()[4]/(1024**3):.2f} GB</code>\n"
        f"RAM Percent: <code>{psutil.virtual_memory()[2]} %</code>\n\n"
        f"• RAM (Swap)\n"
        f"RAM Total (Swap): <code>{psutil.swap_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"RAM Used (Swap): <code>{psutil.swap_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"RAM Free (Swap): <code>{psutil.swap_memory()[2]/(1024**3):.2f} GB</code>\n"
        f"RAM Percent (Swap): <code>{psutil.swap_memory()[3]} %</code>\n\n"
        f"• Drive/Storage\n"
        f"Total Partitions: <code>{len(psutil.disk_partitions())}</code>\n"
        f"Disk Usage Total: <code>{psutil.disk_usage('/')[0]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Used: <code>{psutil.disk_usage('/')[1]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Free: <code>{psutil.disk_usage('/')[2]/(1024**3):.2f} GB</code>\n"
        f"Disk Usage Percent: <code>{psutil.disk_usage('/')[3]} %</code>\n\n"
    )
    await Message.reply_msg(update, sys_info)


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.message.text or update.message.caption if update.message else None

    if chat.type == "private" and msg:
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        # status
        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        # Trigger
        if echo_status == "on":
            await Message.reply_msg(update, msg)

        if auto_tr_status == "on":
            lang_code = find_user.get("lang")
            try:
                tr_msg = translate(msg, lang_code)
            except Exception as e:
                logger.error(f"Error Translator: {e}")
                lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
                btn_name = ["Language Code List 📃"]
                btn_url = [lang_code_list]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
                return
            # tanslate proccess
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)

    # group's
    elif chat.type in ["group", "supergroup"] and msg:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if not find_group:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        # status
        echo_status = find_group.get("echo")
        auto_tr_status = find_group.get("auto_tr")

        # Trigger
        if echo_status == "on":
            await Message.reply_msg(update, msg)
            
        if auto_tr_status == "on":
            lang_code = find_group.get("lang")
            try:
                tr_msg = translate(msg, lang_code)
            except Exception as e:
                logger.error(f"Error Translator: {e}")
                lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
                btn_name = ["Language Code List 📃"]
                btn_url = [lang_code_list]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use <code>/setlang lang_code</code> to set your language.\nE.g. <code>/setlang en</code> if your language is English.", btn)
                return
            # tanslate proccess
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)


def server_alive():
    asyncio.run(ex_server_alive())


async def ex_server_alive():
    server_url = await MongoDB.get_data("bot_docs", "server_url")
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    try:
        if not bot_status or bot_status == "alive":
            await Message.send_msg(owner_id, "Bot Started!")
        elif bot_status == "restart":
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
            await Message.send_msg(owner_id, "Bot Restarted!")
    except Exception as e:
        logger.info(f"Error startup_msg: {e}")

    if len(server_url) != 0:
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        while True:
            try:
                response = requests.get(server_url)
                if response.status_code == 200:
                    logger.info(f"{server_url} is up and running. ✅")
                else:
                    logger.warning(f"{server_url} is down or unreachable. ❌")
            except Exception as e:
                logger.error(f"Error server_alive: {server_url} > {e}")
            await asyncio.sleep(180) # 3 min
    else:
        logger.warning("Server URL not provided !!")


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", func_start, block=False))
    application.add_handler(CommandHandler("movie", func_movieinfo, block=False))
    application.add_handler(CommandHandler("tr", func_translator, block=False))
    application.add_handler(CommandHandler("setlang", func_setlang, block=False))
    application.add_handler(CommandHandler("decode", func_b64decode, block=False))
    application.add_handler(CommandHandler("encode", func_b64encode, block=False))
    application.add_handler(CommandHandler("shortener", func_shortener, block=False))
    application.add_handler(CommandHandler("ping", func_ping, block=False))
    application.add_handler(CommandHandler("calc", func_calc, block=False))
    application.add_handler(CommandHandler("echo", func_echo, block=False))
    application.add_handler(CommandHandler("webshot", func_webshot, block=False))
    application.add_handler(CommandHandler("weather", func_weather, block=False))
    application.add_handler(CommandHandler("imagine", func_imagine, block=False))
    application.add_handler(CommandHandler("chatgpt", func_chatgpt, block=False))
    application.add_handler(CommandHandler("ytdl", func_ytdl, block=False))
    application.add_handler(CommandHandler("yts", func_yts, block=False))
    application.add_handler(CommandHandler("stats", func_stats, block=False))
    application.add_handler(CommandHandler("id", func_id, block=False))
    application.add_handler(CommandHandler("welcome", func_welcome, block=False))
    application.add_handler(CommandHandler("goodbye", func_goodbye, block=False))
    application.add_handler(CommandHandler("antibot", func_antibot, block=False))
    application.add_handler(CommandHandler("invite", func_invite_link, block=False))
    application.add_handler(CommandHandler("pin", func_pin_msg, block=False))
    application.add_handler(CommandHandler("unpin", func_unpin_msg, block=False))
    application.add_handler(CommandHandler("ban", func_ban, block=False))
    application.add_handler(CommandHandler("unban", func_unban, block=False))
    application.add_handler(CommandHandler("kick", func_kick, block=False))
    application.add_handler(CommandHandler("kickme", func_kickme, block=False))
    application.add_handler(CommandHandler("mute", func_mute, block=False))
    application.add_handler(CommandHandler("unmute", func_unmute, block=False))
    application.add_handler(CommandHandler("lockchat", func_lockchat, block=False))
    application.add_handler(CommandHandler("unlockchat", func_unlockchat, block=False))
    application.add_handler(CommandHandler("adminlist", func_adminlist, block=False))
    application.add_handler(CommandHandler("help", func_help, block=False))
    # owner
    application.add_handler(CommandHandler("broadcast", func_broadcast, block=False))
    application.add_handler(CommandHandler("database", func_database, block=False))
    application.add_handler(CommandHandler("cleardb", func_cleardb, block=False))
    application.add_handler(CommandHandler("bsetting", func_bsetting, block=False))
    application.add_handler(CommandHandler("shell", func_shell, block=False))
    application.add_handler(CommandHandler("render", func_render, block=False))
    application.add_handler(CommandHandler("sys", func_sys, block=False))
    # filters
    application.add_handler(MessageHandler(filters.ALL, func_filter_all, block=False))
    # Chat Member Handler
    application.add_handler(ChatMemberHandler(track_chat_activities, ChatMemberHandler.CHAT_MEMBER))
    # Callback button
    application.add_handler(CallbackQueryHandler(func_callbackbtn, block=False))
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    logger.info("🤖 Bot Started !!")
    thread = threading.Thread(target=server_alive)
    thread.start()
    main()
