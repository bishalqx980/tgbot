import os
import sys
import time
import psutil
import random
import asyncio
import requests
import subprocess
from threading import Thread
from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ChatMemberHandler
from bot import logger, bot_token, bot, owner_id
from bot.modules.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from bot.modules.ping import ping_url
from bot.modules.shortener import shortener_url
from bot.modules.translator import translate
from bot.modules.base64 import BASE64
from bot.modules.omdb_movie_info import get_movie_info
from bot.modules.utils import calc
from bot.modules.safone import Safone
from bot.modules.group_management import (
    _check_permission,
    track_my_chat_activities,
    track_chat_activities,
    _check_del_cmd,
    func_invite_link,
    func_promote,
    func_demote,
    func_pin_msg,
    func_unpin_msg,
    func_ban,
    func_unban,
    func_kick,
    func_kickme,
    func_mute,
    func_unmute,
    func_del,
    func_purge,
    func_lockchat,
    func_unlockchat,
    func_filter,
    func_remove,
    func_filters,
    func_adminlist)
from bot.modules.ytdl import YouTubeDownload
from bot.helper.callbackbtn_helper import func_callbackbtn
from bot.modules.weather import weather_info
from bot.modules.g4f import G4F
from bot.update_db import update_database
from bot.modules.qr import QR
from bot.modules.telegraph import TELEGRAPH
from bot.modules.re_link_domain import RE_LINK


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_msg(update, msg)
        return
    
    try:
        _bot_info = await bot.get_me()

        try:
            _bot = context.bot_data["db_bot_data"]
        except Exception as e:
            logger.error(e)
            find = await MongoDB.find("bot_docs", "_id")
            _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
            context.bot_data["db_bot_data"] = _bot

        bot_pic = _bot.get("bot_pic")
        welcome_img = _bot.get("welcome_img")
        support_chat = _bot.get("support_chat")

        msg = (
            f"Hi {user.mention_html()}! I'm <a href='https://t.me/{_bot_info.username}'>{_bot_info.first_name}</a>, your all-in-one bot!\n\n"
            f"<blockquote>Here's a short summary of what I can do:\n\n" # break
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
            f"<i>More Feature coming soon...</i>"
        )

        if _bot_info.username != "MissCiri_bot":
            msg += "\n\nCloned bot of @MissCiri_bot"

        btn_name_1 = ["Add in Group"]
        btn_url_1 = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn_name_2 = ["Developer", "Source Code"]
        btn_url_2 = [f"https://t.me/bishalqx980", "https://github.com/bishalqx980/tgbot"]
        btn_name_3 = ["Support Chat"]
        btn_url_3 = [support_chat]
        btn_1 = await Button.ubutton(btn_name_1, btn_url_1)
        btn_2 = await Button.ubutton(btn_name_2, btn_url_2, True)
        btn = btn_1 + btn_2
        if support_chat:
            try:
                btn_3 = await Button.ubutton(btn_name_3, btn_url_3)
                btn = btn_1 + btn_2 + btn_3
            except Exception as e:
                logger.error(e)
        
        if welcome_img and bot_pic:
            await Message.send_img(user.id, bot_pic, msg, btn)
        else:
            await Message.send_msg(user.id, msg, btn)
        
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True
            }

            try:
                await MongoDB.insert_single_data("users", data)
            except Exception as e:
                logger.error(e)
        
        if chat.type != "private":
            _bot_info = await bot.get_me()
            await Message.reply_msg(update, f"Sent in your pm! <a href='http://t.me/{_bot_info.username}'>Check</a>")
    
    except Forbidden:
        _bot_info = await bot.get_me()
        await Message.reply_msg(update, f"Hola, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
    
    except Exception as e:
        logger.error(e)


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
        f"<pre>{plot}</pre>\n"
    )
    btn_name = [f"✨ IMDB - {title}"]
    btn_url = [f"https://www.imdb.com/title/{imdb_id}"]
    btn = await Button.ubutton(btn_name, btn_url)
    await Message.send_img(chat.id, poster, msg, btn)     


async def func_translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    msg = re_msg.text_html or re_msg.caption_html if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/tr text</code> or reply the text with <code>/tr</code>\nE.g. <code>/tr the text you want to translate</code>\n\nEnable auto translator mode from /settings")
        return
    
    if chat.type == "private":
        try:
            find_user = context.chat_data["db_user_data"]
        except Exception as e:
            logger.error(e)
            find_user = None
        
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
            if find_user:
                context.chat_data["db_user_data"] = find_user
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
            
        lang_code = find_user.get("lang")
    else:
        try:
            find_group = context.chat_data["db_group_data"]
        except Exception as e:
            logger.error(e)
            find_group = None
        
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                context.chat_data["db_group_data"] = find_group
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
            
        lang_code = find_group.get("lang")

    try:
        tr_msg = await translate(msg, lang_code)
    except Exception as e:
        logger.error(e)
        try:
            _bot = context.bot_data["db_bot_data"]
        except Exception as e:
            logger.error(e)
            find = await MongoDB.find("bot_docs", "_id")
            _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
            context.bot_data["db_bot_data"] = _bot
            
        btn_name = ["Language code's"]
        btn_url = ["https://telegra.ph/Language-Code-12-24"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
        return

    if tr_msg != msg:
        await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await Message.reply_msg(update, "Error: Translated text & main text are same!")


async def func_b64decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if not msg:
        if re_msg:
            msg = re_msg.text or re_msg.caption
        else:
            await Message.reply_msg(update, "Use <code>/decode the `Encoded` text</code>\nor reply the `Encoded` text with <code>/decode</code>\nE.g. <code>/decode the `Encoded` text you want to decode</code>")
            return
    
    decode = await BASE64.decode(msg)
    if decode:
        await Message.reply_msg(update, f"<code>{decode}</code>")
    else:
        await Message.reply_msg(update, f"Invalid base64!")


async def func_b64encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if not msg:
        if re_msg:
            msg = re_msg.text or re_msg.caption
        else:
            await Message.reply_msg(update, "Use <code>/encode the `Decoded` or `normal` text</code>\nor reply the `Decoded` or `normal` text with <code>/encode</code>\nE.g. <code>/encode the `Decoded` or `normal` text you want to encode</code>")
            return
    
    encode = await BASE64.encode(msg)
    if encode:
        await Message.reply_msg(update, f"<code>{encode}</code>")
    else:
        await Message.reply_msg(update, f"Invalid text!")


async def func_shortener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/short url</code>\nor reply the url with <code>/short</code>\nE.g. <code>/short https://google.com</code>")
        return
    
    shorted_url = await shortener_url(msg)
    if shorted_url == 0:
        msg = "shrinkme_api not found!"
    elif shorted_url:
        msg = shorted_url
    else:
        msg = "Invalid url!"
    await Message.reply_msg(update, msg)


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)

    if not url:
        await Message.reply_msg(update, "Use <code>/ping url</code>\nE.g. <code>/ping https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_msg(update, f"Pinging {url}\nPlease wait...")
    ping = await ping_url(url)

    if not ping:
        await Message.edit_msg(update, "Something went wrong!", sent_msg)
        return

    try:
        ping_time, status_code = ping
        if status_code == 200:
            site_status = "online"
        else:
            site_status = "offline"

        msg = (
            f"Site: {url}\n"
            f"R.time(ms): <code>{ping_time}</code>\n"
            f"R.code: <code>{status_code}</code>\n"
            f"Status: {site_status}"
        )
        await Message.edit_msg(update, msg, sent_msg)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error: {e}", sent_msg)


async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/calc math</code>\nor reply the math with <code>/calc</code>\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")
        return
    
    try:
        await Message.reply_msg(update, f"Calculation result: <code>{await calc(msg):.2f}</code>")
    except Exception as e:
        logger.error(e)
        await Message.reply_msg(update, f"Can't calc: {e}")   


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
        logger.error(e)
        await Message.reply_msg(update, f"Error: {e}")      


async def func_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args)

    if not location:
        await Message.reply_msg(update, "Use <code>/weather location_name</code>\nE.g. <code>/weather london</code>")
        return
    
    info = await weather_info(location)

    if not info:
        await Message.reply_msg(update, "weather_api not found!")
        return
    
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
    user = update.effective_user
    chat = update.effective_chat
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine a cute cat</code>")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")
    retry = 0

    while retry != 2:
        imagine = await Safone.imagine(prompt)
        if imagine:
            break
        elif retry == 2:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, Imagine is busy!\nAttempt: {retry}", sent_msg)
        await asyncio.sleep(3)
    
    try:
        await Message.send_img(chat.id, imagine, f"» <i>{prompt}</i>\n<b>Req by</b>: {user.mention_html()}")
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error Imagine: {e}", sent_msg, parse_mode=ParseMode.MARKDOWN)


async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "Use <code>/gpt your_prompt</code>\nE.g. <code>/gpt What is AI?</code>")
        return
    
    common_words = ["hi", "hello"]
    if prompt.lower() in common_words:
        await Message.reply_msg(update, "Hello! How can I assist you today?")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")
    retry = 0

    while retry != 3:
        g4f_gpt = await G4F.chatgpt(f"{prompt}, explain in few sentences and in English.")
        if g4f_gpt and "流量异常, 请尝试更换网络环境, 如果你觉得ip被误封了, 可尝试邮件联系我们, 当前" not in g4f_gpt:
            break
        elif retry == 3:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, ChatGPT is busy!\nAttempt: {retry}", sent_msg)
        await asyncio.sleep(3)
    
    try:
        await Message.edit_msg(update, g4f_gpt, sent_msg, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error ChatGPT: {e}", sent_msg, parse_mode=ParseMode.MARKDOWN)


async def func_ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    url = re_msg.text if re_msg else " ".join(context.args)

    if chat.type != "private":
        _bot_info = await bot.get_me()
        btn_name = ["Start me in private"]
        btn_url = [f"http://t.me/{_bot_info.username}?start=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.reply_msg(update, f"Coming Soon...\nYou can use this feature in bot private chat!", btn)
        return
    
    if not url:
        await Message.reply_msg(update, "Use <code>/ytdl youtube_url</code> to download a video!")
        return
    
    context.chat_data["user_id"] = user.id
    context.chat_data["del_msg_pointer"] = e_msg
    
    btn_name_row1 = ["Video (mp4)", "Audio (mp3)"]
    btn_data_row1 = ["mp4", "mp3"]

    btn_name_row2 = ["Cancel"]
    btn_data_row2 = ["close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2)

    btn = row1 + row2

    del_msg = await Message.reply_msg(update, f"\nSelect <a href='{url}'>Content</a> Quality/Format", btn, disable_web_preview=False)

    timeout = 0

    while timeout < 15:
        content_format = context.user_data.get("content_format")
        timeout += 1
        await asyncio.sleep(1)
        if content_format:
            context.user_data["content_format"] = None
            break
    
    await Message.del_msg(chat.id, del_msg)

    if not content_format:
        await Message.reply_msg(update, "Timeout!")
        return
    
    sent_msg = await Message.reply_msg(update, "Please Wait...")
    await Message.edit_msg(update, "📥 Downloading...", sent_msg)

    res = await YouTubeDownload.ytdl(url, content_format)
    
    if res[0] == 0:
        await Message.edit_msg(update, res[1], sent_msg)
        return

    await Message.edit_msg(update, "📤 Uploading...", sent_msg)

    try:
        if content_format == "mp4":
            title, file_path, thumbnail = res
            await Message.send_vid(chat.id, file_path, thumbnail, title, e_msg.id)
        elif content_format == "mp3":
            title, file_path = res
            await Message.send_audio(chat.id, file_path, title, title, e_msg.id)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error Uploading: {e}", sent_msg)

    try:
        if len(res) == 3:
            rem_files = [res[1], res[2]]
        else:
            rem_files = [res[1]]
        for rem in rem_files:
            os.remove(rem)
            logger.info(f"{rem} Removed...")
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(e) 


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


async def func_gen_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    data = " ".join(context.args)

    if not data:
        await Message.reply_msg(update, "Use <code>/qr url/data/text</code> to generate a QR code img...\nE.g. <code>/qr https://google.com</code>")
        return

    sent_msg = await Message.reply_msg(update, f"Generating...")
    gen_qr = await QR.gen_qr(data)

    if not gen_qr:
        await Message.edit_msg(update, "Something went wrong!", sent_msg)
        return

    try:
        await Message.send_img(chat.id, gen_qr, data)
        os.remove(gen_qr)
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error: {e}", sent_msg)


async def func_img_to_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    if re_msg:
        photo = re_msg.photo[-1] if re_msg.photo else None

    if not re_msg or not photo:
        await Message.reply_msg(update, "Reply a photo to get a public link for that photo!")
        return
    
    sent_msg = await Message.reply_msg(update, f"Generating public link...")
    photo = await bot.get_file(photo.file_id)
    dir_name = "download/telegraph/"
    os.makedirs(dir_name, exist_ok=True)
    f_name = f"{dir_name}image.png"
    req = requests.get(photo.file_path)
    with open(f_name, "wb") as f:
        f.write(req.content)
    
    itl = await TELEGRAPH.upload_img(f_name)
    if not itl:
        await Message.edit_msg(update, "Something went wrong!", sent_msg)
        return

    try:
        await Message.edit_msg(update, itl, sent_msg)
        os.remove(f_name)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error: {e}", sent_msg)


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    try:
        _bot = context.bot_data["db_bot_data"]
    except Exception as e:
        logger.error(e)
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        context.bot_data["db_bot_data"] = _bot

    if chat.type == "private":
        try:
            find_user = context.chat_data["db_user_data"]
        except Exception as e:
            logger.error(e)
            find_user = None
        
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
            if find_user:
                context.chat_data["db_user_data"] = find_user
            else:
                await Message.reply_msg(update, "User data not found! Block me then start me again! (no need to delete chat)")
                return
        
        user_mention = find_user.get("mention")
        lang = find_user.get("lang")
        echo = find_user.get("echo")
        auto_tr = find_user.get("auto_tr")

        context.chat_data["edit_cname"] = "users"
        context.chat_data["find_data"] = "user_id"
        context.chat_data["match_data"] = user.id
        context.chat_data["chat_id"] = chat.id
        context.chat_data["user_id"] = user.id
        context.chat_data["del_msg_pointer"] = e_msg

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• User: {user_mention}\n"
            f"• ID: <code>{user.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n\n"
        )

        btn_name_row1 = ["Language", "Auto translate"]
        btn_data_row1 = ["lang", "auto_tr"]

        btn_name_row2 = ["Echo", "Close"]
        btn_data_row2 = ["set_echo", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        try:
            images = await MongoDB.get_data("bot_docs", "images")
            if images:
                image = random.choice(images).strip()
            else:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(chat.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(chat.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat.id, msg, btn)

    elif chat.type in ["group", "supergroup"]:
        await _check_del_cmd(update, context)

        if user.is_bot:
            await Message.reply_msg(update, "I don't take permission from anonymous admins!")
            return

        _chk_per = await _check_permission(update, user=user)

        if not _chk_per:
            return
        
        _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
            
        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.reply_msg(update, "I'm not an admin in this chat!")
            return
        
        if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            await Message.reply_msg(update, "You aren't an admin in this chat!")
            return
        
        if user_permission.status == ChatMember.ADMINISTRATOR:
            if not admin_rights.get("can_change_info"):
                await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
                return

        try:
            find_group = context.chat_data["db_group_data"]
        except Exception as e:
            logger.error(e)
            find_group = None
        
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                context.chat_data["db_group_data"] = find_group
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        if not find_group:
            await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
            return
        
        title = find_group.get("title")
        lang = find_group.get("lang")

        echo = find_group.get("echo")
        auto_tr = find_group.get("auto_tr")
        welcome_msg = find_group.get("welcome_msg")
        goodbye_msg = find_group.get("goodbye_msg")
        antibot = find_group.get("antibot")
        del_cmd = find_group.get("del_cmd")
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        log_channel = find_group.get("log_channel")

        context.chat_data["edit_cname"] = "groups"
        context.chat_data["find_data"] = "chat_id"
        context.chat_data["match_data"] = chat.id
        context.chat_data["chat_id"] = chat.id
        context.chat_data["user_id"] = user.id
        context.chat_data["del_msg_pointer"] = e_msg

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• Title: {title}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Welcome user: <code>{welcome_msg}</code>\n"
            f"• Goodbye user: <code>{goodbye_msg}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
            f"• Delete cmd: <code>{del_cmd}</code>\n"
            f"• All links: <code>{all_links}</code>\n"
            f"• Allowed links: <code>{allowed_links}</code>\n"
            f"• Log channel: <code>{log_channel}</code>\n"
        )

        btn_name_row1 = ["Language", "Auto translate"]
        btn_data_row1 = ["lang", "auto_tr"]

        btn_name_row2 = ["Echo", "Anti bot"]
        btn_data_row2 = ["set_echo", "antibot"]

        btn_name_row3 = ["Welcome", "Goodbye"]
        btn_data_row3 = ["welcome_msg", "goodbye_msg"]

        btn_name_row4 = ["Delete cmd", "Log channel"]
        btn_data_row4 = ["del_cmd", "log_channel"]

        btn_name_row5 = ["Links", "Close"]
        btn_data_row5 = ["links_behave", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

        btn = row1 + row2 + row3 + row4 + row5

        try:
            images = await MongoDB.get_data("bot_docs", "images")
            if images:
                image = random.choice(images).strip()
            else:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(chat.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(chat.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat.id, msg, btn)


async def func_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message

    if re_msg:
        if re_msg.forward_from:
            from_user_id = re_msg.forward_from.id
        elif re_msg.from_user:
            from_user_id = re_msg.from_user.id

    if chat.type == "private":
        if re_msg:
            if user.id == from_user_id:
                msg = (
                    f"• Your UserID: <code>{user.id}</code>\n"
                    f"<i>Replied user account is hidden! Can't get user_id</i>"
                )
            else:
                msg = (
                    f"• Your UserID: <code>{user.id}</code>\n"
                    f"• Replied UserID: <code>{from_user_id}</code>"
                )
        else:
            msg = (
                f"• UserID: <code>{user.id}</code>"
            )
        await Message.reply_msg(update, msg)

    elif chat.type in ["group", "supergroup"]:
        if re_msg:
            msg = (
                f"• Your UserID: <code>{user.id}</code>\n"
                f"• Replied UserID: <code>{from_user_id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            ) 
        else:
            msg = (
                f"• UserID: <code>{user.id}</code>\n"
                f"• ChatID: <code>{chat.id}</code>"
            )
        await Message.reply_msg(update, msg)


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    
    try:
        db = await MongoDB.info_db()
        for i in db:
            if i[0] == "users":
                total_users = i[1]
                break
            else:
                total_users = "❓"
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        msg = (
            f"Hi {user.mention_html()}! Welcome to the bot help section...\n"
            f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
            f"/start - to start the bot\n"
            f"/help - to see this message\n\n"
            f"T.users: {total_users} | "
            f"A.users: {active_users} | "
            f"Inactive: {inactive_users}"
        )

        context.chat_data["user_id"] = user.id
        context.chat_data["del_msg_pointer"] = e_msg

        btn_name_row1 = ["Group Management", "Artificial intelligence"]
        btn_data_row1 = ["group_management", "ai"]

        btn_name_row2 = ["misc", "Bot owner"]
        btn_data_row2 = ["misc_func", "owner_func"]

        btn_name_row3 = ["GitHub", "Close"]
        btn_data_row3 = ["github_stats", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        try:
            images = await MongoDB.get_data("bot_docs", "images")
            if images:
                image = random.choice(images).strip()
            else:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(user.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(user.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(user.id, msg, btn)
        
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True
            }

            try:
                await MongoDB.insert_single_data("users", data)
            except Exception as e:
                logger.error(e)
        
        if chat.type != "private":
            _bot_info = await bot.get_me()
            await Message.reply_msg(update, f"Sent in your pm! <a href='http://t.me/{_bot_info.username}'>Check</a>")

    except Forbidden:
        _bot_info = await bot.get_me()
        await Message.reply_msg(update, f"Hola, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
        
    except Exception as e:
        logger.error(e)


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    replied_msg = update.message.reply_to_message
    inline_text = " ".join(context.args)

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    msg = replied_msg.text_html or replied_msg.caption_html if replied_msg else None

    if not replied_msg:
        await Message.reply_msg(update, "Reply a message to broadcast!\n<code>/broadcast f</code> to forwared message!")
        return
    
    forward_confirm, to_whom = None, None

    if inline_text:
        inline_text_split = inline_text.split()
        if len(inline_text_split) == 2:
            forward_confirm, to_whom = inline_text_split
        elif len(inline_text_split) == 1:
            if inline_text_split[0] == "f":
                forward_confirm = True
            else:
                to_whom = inline_text_split[0]
    
    if to_whom:
        try: 
            user_id = to_whom
            if forward_confirm:
                await Message.forward_msg(user_id, chat.id, replied_msg.id)
            else:
                if msg:
                    if replied_msg.text_html:
                        await Message.send_msg(user_id, msg)
                    elif replied_msg.caption:
                        await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)
                else:
                    await Message.reply_msg(update, "Message to broadcast, not found!")
                    return
            await Message.reply_msg(update, "<i>Message Sent...!</i>")
        except Exception as e:
            logger.error(e)
            await Message.reply_msg(update, f"Error Broadcast: {e}")
        return
    
    users_id = await MongoDB.find("users", "user_id")
    active_status = await MongoDB.find("users", "active_status")

    if len(users_id) == len(active_status):
        combined_list = list(zip(users_id, active_status))
        active_users = []
        for filter_user_id in combined_list:
            if filter_user_id[1] == True:
                active_users.append(filter_user_id[0])
    else:
        await Message.reply_msg(update, f"Error: Users {len(user_id)} not equal to active_status {len(active_status)}...!")
        return

    sent_count, except_count = 0, 0
    notify = await Message.send_msg(user.id, f"Total Users: {len(users_id)}\nActive Users: {len(active_users)}")
    start_time = time.time()
    for user_id in active_users:
        try:
            if forward_confirm:
                await Message.forward_msg(user_id, chat.id, replied_msg.id)
            else:
                if msg:
                    if replied_msg.text_html:
                        await Message.send_msg(user_id, msg)
                    elif replied_msg.caption:
                        await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)
                else:
                    await Message.reply_msg(update, "Message to broadcast, not found!")
                    await Message.del_msg(chat.id, notify)
                    return
            sent_count += 1
            progress = (sent_count + except_count) * 100 / len(active_users)
            await Message.edit_msg(update, f"Total Users: {len(users_id)}\nActive Users: {len(active_users)}\nSent: {sent_count}\nException occurred: {except_count}\nProgress: {int(progress)}%", notify)
            # sleep for 0.5sec
            await asyncio.sleep(0.5)
        except Exception as e:
            except_count += 1
            logger.error(e)
    end_time = time.time()
    await Message.reply_msg(update, f"<i>Broadcast Done...!\nTime took: {(end_time - start_time):.2f}</i>")


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    chat_id = " ".join(context.args)

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if chat_id:
        if "-100" in str(chat_id):
            find_group = await MongoDB.find_one("groups", "chat_id", int(chat_id))
            if not find_group:
                await Message.reply_msg(update, "Chat not found!")
                return
            
            title = find_group.get("title")
            chat_id = find_group.get("chat_id")
            lang = find_group.get("lang")
            echo = find_group.get("echo")
            auto_tr = find_group.get("auto_tr")
            welcome_msg = find_group.get("welcome_msg")
            custom_welcome_msg = find_group.get("custom_welcome_msg")
            goodbye_msg = find_group.get("goodbye_msg")
            antibot = find_group.get("antibot")
            del_cmd = find_group.get("del_cmd")
            all_links = find_group.get("all_links")
            allowed_links = find_group.get("allowed_links")
            log_channel = find_group.get("log_channel")
            filters = find_group.get("filters")
            if filters:
                storage = ""
                for key in filters:
                    storage += f"» {key}: {filters[key]}\n"

            msg = (
                f"<code>Title         :</code> {title}\n"
                f"<code>ID            :</code> <code>{chat_id}</code>\n"
                f"<code>Lang          :</code> {lang}\n"
                f"<code>Echo          :</code> {echo}\n"
                f"<code>Auto tr       :</code> {auto_tr}\n"
                f"<code>Welcome       :</code> {welcome_msg}\n"
                f"<blockquote>{custom_welcome_msg}</blockquote>\n"
                f"<code>Farewell      :</code> {goodbye_msg}\n"
                f"<code>Antibot       :</code> {antibot}\n"
                f"<code>Delete cmd    :</code> {del_cmd}\n"
                f"<code>All links     :</code> {all_links}\n"
                f"<code>Allowed links:</code> {allowed_links}\n"
                f"<code>Log channel   :</code> <code>{log_channel}</code>\n"
                f"<code>Filters       :</code> <blockquote>{storage}</blockquote>\n"
            )
            await Message.reply_msg(update, f"<b>{msg}</b>")
        else:
            find_user = await MongoDB.find_one("users", "user_id", int(chat_id))
            if not find_user:
                await Message.reply_msg(update, "User not found!")
                return
            
            Name = find_user.get("Name")
            user_id = find_user.get("user_id")
            username = find_user.get("username")
            mention = find_user.get("mention")
            lang = find_user.get("lang")
            echo = find_user.get("echo")
            active_status = find_user.get("active_status")
            last_used = find_user.get("last_used")

            msg = (
                f"<code>Name     :</code> {Name}\n"
                f"<code>Mention  :</code> {mention}\n"
                f"<code>ID       :</code> <code>{user_id}</code>\n"
                f"<code>Username :</code> @{username}\n"
                f"<code>Lang     :</code> {lang}\n"
                f"<code>Echo     :</code> {echo}\n"
                f"<code>A. status:</code> {active_status}\n"
                f"<code>Last used:</code> {last_used}\n"
            )
            await Message.reply_msg(update, f"<b>{msg}</b>")
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
    active_status = await MongoDB.find("users", "active_status")
    active_users = active_status.count(True)
    inactive_users = active_status.count(False)
    await Message.reply_msg(update, f"<b>{msg}Active users: {active_users}\nInactive users: {inactive_users}</b>")


async def func_bsetting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    welcome_img = await MongoDB.get_data("bot_docs", "welcome_img")
    
    context.chat_data["edit_cname"] = "bot_docs"
    context.chat_data["find_data"] = "welcome_img"
    context.chat_data["match_data"] = welcome_img
    context.chat_data["chat_id"] = chat.id
    context.chat_data["user_id"] = user.id
    context.chat_data["del_msg_pointer"] = e_msg
    
    btn_name_row1 = ["Bot pic", "Welcome img"]
    btn_data_row1 = ["bot_pic", "welcome_img"]

    btn_name_row2 = ["Images", "Support chat"]
    btn_data_row2 = ["images", "support_chat"]

    btn_name_row3 = ["GitHub", "Server url", "Sudo"]
    btn_data_row3 = ["github_repo", "server_url", "sudo_users"]

    btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
    btn_data_row4 = ["shrinkme_api", "omdb_api", "weather_api"]

    btn_name_row5 = ["⚠ Restore Settings", "Close"]
    btn_data_row5 = ["restore_db", "close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
    row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
    row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

    btn = row1 + row2 + row3 + row4 + row5

    try:
        images = await MongoDB.get_data("bot_docs", "images")
        if images:
            image = random.choice(images).strip()
        else:
            image = await MongoDB.get_data("bot_docs", "bot_pic")
        await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
    except Exception as e:
        logger.error(e)
        try:
            image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat.id, "<u><b>Bot Settings</b></u>", btn)


async def func_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    command = " ".join(context.args)
    command = command.replace("'", "")

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if not command:
        await Message.reply_msg(update, "E.g. <code>/shell dir/ls</code> [linux/Windows Depend on your hosting device]")
        return
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        if not result.stdout:
            await Message.reply_msg(update, "None")
            return
        with open('shell.txt', 'w') as shell_file:
            shell_file.write(result.stdout)
        with open("shell.txt", "rb") as shell_file:
            shell = shell_file.read()
        await Message.send_doc(chat.id, shell, "shell.txt", command, e_msg.id)
    else:
        await Message.reply_msg(update, result.stderr)


async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    with open("log.txt", "rb") as log_file:
        log = log_file.read()
    await Message.send_doc(chat.id, log, "log.txt", "log.txt", e_msg.id)


async def func_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "Check pm!")
    
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    try:
        if not bot_status or bot_status == "alive":
            await Message.send_msg(user.id, "Restaring...")
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "restart")
            os.execv(sys.executable, ["python"] + sys.argv)
        elif bot_status == "restart":
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
            await Message.send_msg(user.id, "Bot Restarted!")
    except Exception as e:
        logger.error(e)


async def func_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))

    if user.id not in power_users:
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


async def func_filter_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    
    try:
        await Message.del_msg(chat.id, e_msg)
    except Exception as e:
        logger.error(e)


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    msg = update.message.text_html or update.message.caption_html if update.message else None

    if user.id == 777000:
        return

    if context.chat_data.get("status") == "editing":
        try:
            msg = int(msg)
        except:
            msg = msg
        context.chat_data["new_value"] = msg
        context.chat_data["edit_value_del_msg_pointer"] = e_msg
        context.chat_data["status"] = None
        return

    if chat.type == "private" and msg:
        try:
            find_user = context.chat_data["db_user_data"]
        except Exception as e:
            logger.error(e)
            find_user = None
        
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
            if find_user:
                context.chat_data["db_user_data"] = find_user
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        if echo_status:
            await Message.reply_msg(update, msg)

        if auto_tr_status:
            lang_code = find_user.get("lang")
            try:
                tr_msg = await translate(msg, lang_code)
            except Exception as e:
                logger.error(e)
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
                return
            # tanslate proccess
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)

    # group's
    elif chat.type in ["group", "supergroup"] and msg:
        _chk_per = await _check_permission(update, user=user, checking_msg=False)
        if not _chk_per:
            return
        
        _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.send_msg(chat.id, "I'm not an admin in this chat!")
            return
        
        try:
            find_group = context.chat_data["db_group_data"]
        except Exception as e:
            logger.error(e)
            find_group = None
        
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                context.chat_data["db_group_data"] = find_group
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        
        if not allowed_links:
            allowed_links = []
        else:
            storage = []
            for i in allowed_links:
                storage.append(i.strip())
            allowed_links = storage

        echo_status = find_group.get("echo")
        auto_tr_status = find_group.get("auto_tr")
        lang_code = find_group.get("lang")
        filters = find_group.get("filters")

        msg_contains_link = False

        if all_links:
            if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                links_list = await RE_LINK.detect_link(msg)
                if links_list:
                    clean_msg = msg
                    allowed_links_count = 0
                    for link in links_list:
                        domain = await RE_LINK.match_domain(link)
                        if domain in allowed_links:
                            allowed_links_count += 1
                        else:
                            if all_links == "delete":
                                clean_msg = clean_msg.replace(link, f"<code>forbidden link</code>")
                            if all_links == "convert":
                                b64_link = await BASE64.encode(link)
                                clean_msg = clean_msg.replace(link, f"<code>{b64_link}</code>")
                    if allowed_links_count != len(links_list):
                        try:
                            clean_msg = f"{user.mention_html()}\n\n{clean_msg}\n\n<i>Delete reason: your message contains forbidden link/s!</i>"
                            await Message.del_msg(chat.id, e_msg)
                            await Message.send_msg(chat.id, clean_msg)
                            msg_contains_link = True
                        except Exception as e:
                            logger.error(e)
        
        if echo_status and not msg_contains_link:
            await Message.reply_msg(update, msg)
        
        if auto_tr_status and not msg_contains_link:
            try:
                tr_msg = await translate(msg, lang_code)
            except Exception as e:
                logger.error(e)
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
            
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)
        
        if filters:
            for keyword in filters:
                filter_msg = msg.lower() if not isinstance(msg, int) else msg
                if keyword.lower() in filter_msg:
                    filtered_msg = filters[keyword]
                    formattings = {
                        "{first}": user.first_name,
                        "{last}": user.last_name,
                        "{fullname}": user.full_name,
                        "{username}": user.username,
                        "{mention}": user.mention_html(),
                        "{id}": user.id,
                        "{chatname}": chat.title
                    }

                    for key, value in formattings.items():
                        if not value:
                            value = ""
                        filtered_msg = filtered_msg.replace(key, str(value))
                    await Message.reply_msg(update, filtered_msg)


async def server_alive():
    server_url = await MongoDB.get_data("bot_docs", "server_url")
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    sudo_users = await MongoDB.get_data("bot_docs", "sudo_users")
    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))
    
    try:
        if not bot_status or bot_status == "alive":
            for user_id in power_users:
                try:
                    await Message.send_msg(user_id, "Bot Started!")
                except Exception as e:
                    logger.error(e)
        elif bot_status == "restart":
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
            for user_id in power_users:
                try:
                    await Message.send_msg(user_id, "Bot Restarted!")
                except Exception as e:
                    logger.error(e)
    except Exception as e:
        logger.error(e)

    if server_url:
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
                logger.error(f"{server_url} > {e}")
            await asyncio.sleep(180) # 3 min
    else:
        logger.warning("Server URL not provided !!")
        await Message.send_msg(owner_id, "Warning! Server URL not provided!\nGoto /bsetting and setup server url then restart bot...")


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", func_start, block=False))
    application.add_handler(CommandHandler("movie", func_movieinfo, block=False))
    application.add_handler(CommandHandler("tr", func_translator, block=False))
    application.add_handler(CommandHandler("decode", func_b64decode, block=False))
    application.add_handler(CommandHandler("encode", func_b64encode, block=False))
    application.add_handler(CommandHandler("short", func_shortener, block=False))
    application.add_handler(CommandHandler("ping", func_ping, block=False))
    application.add_handler(CommandHandler("calc", func_calc, block=False))
    application.add_handler(CommandHandler("webshot", func_webshot, block=False))
    application.add_handler(CommandHandler("weather", func_weather, block=False))
    application.add_handler(CommandHandler("imagine", func_imagine, block=False))
    application.add_handler(CommandHandler("gpt", func_chatgpt, block=False))
    application.add_handler(CommandHandler("ytdl", func_ytdl, block=False))
    application.add_handler(CommandHandler("yts", func_yts, block=False))
    application.add_handler(CommandHandler("qr", func_gen_qr, block=False))
    application.add_handler(CommandHandler("itl", func_img_to_link, block=False))
    application.add_handler(CommandHandler("settings", func_settings, block=False))
    application.add_handler(CommandHandler("id", func_id, block=False))
    application.add_handler(CommandHandler("invite", func_invite_link, block=False))
    application.add_handler(CommandHandler("promote", func_promote, block=False))
    application.add_handler(CommandHandler("demote", func_demote, block=False))
    application.add_handler(CommandHandler("pin", func_pin_msg, block=False))
    application.add_handler(CommandHandler("unpin", func_unpin_msg, block=False))
    application.add_handler(CommandHandler("ban", func_ban, block=False))
    application.add_handler(CommandHandler("unban", func_unban, block=False))
    application.add_handler(CommandHandler("kick", func_kick, block=False))
    application.add_handler(CommandHandler("kickme", func_kickme, block=False))
    application.add_handler(CommandHandler("mute", func_mute, block=False))
    application.add_handler(CommandHandler("unmute", func_unmute, block=False))
    application.add_handler(CommandHandler("del", func_del, block=False))
    application.add_handler(CommandHandler("purge", func_purge, block=False))
    application.add_handler(CommandHandler("lock", func_lockchat, block=False))
    application.add_handler(CommandHandler("unlock", func_unlockchat, block=False))
    application.add_handler(CommandHandler("filter", func_filter, block=False))
    application.add_handler(CommandHandler("remove", func_remove, block=False))
    application.add_handler(CommandHandler("filters", func_filters, block=False))
    application.add_handler(CommandHandler("adminlist", func_adminlist, block=False))
    application.add_handler(CommandHandler("help", func_help, block=False))
    # owner
    application.add_handler(CommandHandler("broadcast", func_broadcast, block=False))
    application.add_handler(CommandHandler("db", func_database, block=False))
    application.add_handler(CommandHandler("bsetting", func_bsetting, block=False))
    application.add_handler(CommandHandler("shell", func_shell, block=False))
    application.add_handler(CommandHandler("log", func_log, block=False))
    application.add_handler(CommandHandler("restart", func_restart, block=False))
    application.add_handler(CommandHandler("sys", func_sys, block=False))
    # filters
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, func_filter_services, block=False))
    application.add_handler(MessageHandler(filters.ALL, func_filter_all, block=False))
    # Chat Member Handler
    application.add_handler(ChatMemberHandler(track_my_chat_activities, ChatMemberHandler.MY_CHAT_MEMBER)) # for tacking bot/private chat
    application.add_handler(ChatMemberHandler(track_chat_activities, ChatMemberHandler.CHAT_MEMBER)) # for tacking group/supergroup
    # Callback button
    application.add_handler(CallbackQueryHandler(func_callbackbtn, block=False))
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    #Thread(target=start_up_work).start()

    async def start_up_work():
        await update_database()
        await server_alive()
    
    loop = asyncio.get_event_loop()
    loop.create_task(start_up_work())
    loop.create_task(main())
    loop.run_forever()
