import os
import json
import psutil
import random
import asyncio
import requests
import subprocess
from threading import Thread
from datetime import datetime
from telegram.constants import ParseMode
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ChatMemberHandler
from bot import logger, bot_token, bot, owner_id, owner_username
from bot.modules.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from bot.modules.ping import ping_url
from bot.modules.shortener import shortener_url
from bot.modules.translator import translate
from bot.modules.base64 import decode_b64, encode_b64
from bot.modules.omdb_movie_info import get_movie_info
from bot.modules.utils import calc
from bot.modules.safone import Safone
from bot.modules.group_management import (
    _check_permission,
    track_chat_activities,
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
    func_lockchat,
    func_unlockchat,
    func_adminlist)
from bot.modules.ytdl import YouTubeDownload
from bot.helper.callbackbtn_helper import func_callbackbtn
from bot.modules.weather import weather_info
from bot.modules.g4f import G4F
from bot.modules.render import Render
from bot.update_db import update_database


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
    btn_name_2 = ["Developer", "Source Code"]
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

    if not msg:
        await Message.reply_msg(update, "Use <code>/tr text</code> or reply the text with <code>/tr</code>\nE.g. <code>/tr the text you want to translate</code>\n\nEnable auto translator mode from /settings")
        return

    find_chat = await MongoDB.find_one("users", "user_id", user.id)

    if not find_chat:
        find_chat = await MongoDB.find_one("groups", "chat_id", chat.id)
    
    if not find_chat:
        await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
        return
    
    lang_code = find_chat.get("lang")

    try:
        tr_msg = translate(msg, lang_code)
    except Exception as e:
        logger.error(f"Error Translator: {e}")
        lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
        btn_name = ["Language code's"]
        btn_url = [lang_code_list]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
        return

    if tr_msg != msg:
        await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await Message.reply_msg(update, "Error: Translated text & main text are same!")


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
        logger.error(f"Can't calc: {e}")
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

    await Message.reply_msg(update, "Out of order! ❌")
    return

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
        await MongoDB.update_db("users", "user_id", user.id, "last_used", {current_time})
    except Exception as e:
        logger.error(f"Error Imagine: {e}")
        await Message.reply_msg(update, f"Error Imagine: {e}")


async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_msg(update, "Use <code>/gpt your_prompt</code>\nE.g. <code>/gpt What is AI?</code>")
        return

    ignore_words = ["hi", "hello", "how are you", "how are you?"]
    if prompt.lower() in ignore_words:
        await Message.reply_msg(update, "I'm not a chatbot! I was made for answering complex questions...")
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
                        await Message.reply_msg(update, "Usage limit exceeded! Check bot private message!")
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

    retry_gpt = 0

    while retry_gpt != 3:
        g4f_gpt = await G4F.chatgpt(f"{prompt}, tell me under 300 words.")
        retry_gpt += 1
        await Message.edit_msg(update, f"Please wait, ChatGPT is busy!\nAttempt: {retry_gpt}", sent_msg)
        await asyncio.sleep(3)
        if g4f_gpt and "流量异常, 请尝试更换网络环境, 如果你觉得ip被误封了, 可尝试邮件联系我们, 当前" not in g4f_gpt:
            break
        elif retry_gpt == 3:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
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
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    url = re_msg.text if re_msg else " ".join(context.args)

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
    
    context.chat_data["user_id"] = user.id
    
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
            break
    
    await Message.del_msg(chat.id, del_msg)

    if not content_format:
        await Message.reply_msg(update, "Timeout!")
        return
    
    sent_msg = await Message.reply_msg(update, "Please Wait...")
    await Message.edit_msg(update, "📥 Downloading...", sent_msg)

    res = YouTubeDownload.ytdl(url, content_format)

    if not res:
        await Message.edit_msg(update, "Something Went Wrong...", sent_msg)
        return

    await Message.edit_msg(update, "📤 Uploading...", sent_msg)

    try_attempt, max_attempt = 0, 3

    while try_attempt != max_attempt:
        try:
            if content_format == "mp4":
                title, file_path, thumbnail = res
                await Message.send_vid(chat.id, file_path, thumbnail, title, e_msg.id)
            elif content_format == "mp3":
                title, file_path = res
                await Message.send_audio(chat.id, file_path, title, title, e_msg.id)
                break
        except Exception as e:
            logger.error(f"Error Uploading: {e}")
            try_attempt += 1
            await Message.edit_msg(update, f"📤 Uploading... [Retry Attempt: {try_attempt}/{max_attempt}]", sent_msg)
            if try_attempt == max_attempt:
                logger.error(f"Error Uploading: {e}")
                await Message.send_msg(chat.id, f"Error Uploading: {e}")
                break
            logger.info(f"Waiting {2**try_attempt}sec before retry...")
            await asyncio.sleep(2**try_attempt)
    try:
        if len(res) >= 3:
            rem_files = [res[1], res[2]]
        else:
            rem_files = [res[1]]
        for rem in rem_files:
            os.remove(rem)
            logger.info(f"{rem} Removed...")
        await Message.del_msg(chat.id, sent_msg)
    except Exception as e:
        logger.error(f"Error os.remove: {e}")  


async def func_yts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = " ".join(context.args)

    if not keyword:
        await Message.reply_msg(update, "Use <code>/yts keyword</code>\nE.g. <code>/yts google keynote</code>")
        return
    
    result = YouTubeDownload.yts(keyword)
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


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    chat_id = " ".join(context.args)

    if chat.type == "private":
        if chat_id:
            if user.id != int(owner_id):
                await Message.reply_msg(update, f"Access Denied! [owner only]")
                return
            else:
                chat_id = int(chat_id)
        else:
            chat_id = user.id

        find_user = await MongoDB.find_one("users", "user_id", chat_id)

        if not find_user:
            find_group = await MongoDB.find_one("groups", "chat_id", chat_id)
        
            if not find_group:
                await Message.reply_msg(update, "User/Chat not found!")
                return

        if find_user:
            user_mention = find_user.get("mention")

            lang = find_user.get("lang")
            echo = find_user.get("echo")
            auto_tr = find_user.get("auto_tr")

            chatgpt_req = find_user.get("chatgpt_req")
            ai_imagine_req = find_user.get("ai_imagine_req")
            
            chatgpt_limit = await MongoDB.get_data("bot_docs", "chatgpt_limit")
            ai_imagine_limit = await MongoDB.get_data("bot_docs", "ai_imagine_limit")

            last_used = find_user.get("last_used")

            premium_users = await MongoDB.get_data("bot_docs", "premium_users")
            if not premium_users:
                is_premium = False
            else:
                is_premium = True if chat_id in premium_users else False

            
            context.chat_data["edit_cname"] = "users"
            context.chat_data["find_data"] = "user_id"
            context.chat_data["match_data"] = chat_id
            context.chat_data["chat_id"] = chat.id
            context.chat_data["user_id"] = user.id

            msg = (
                f"<b>Chat Settings</b> -\n\n"
                f"• User: {user_mention}\n"
                f"• ID: <code>{chat_id}</code>\n"
                f"• Is premium: <code>{is_premium}</code>\n\n"

                f"• Lang: <code>{lang}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n\n"

                f"• ChatGPT: <code>{chatgpt_req}/{chatgpt_limit}</code>\n"
                f"• AI imagine: <code>{ai_imagine_req}/{ai_imagine_limit}</code>\n"
                f"• Last used: <code>{last_used}</code>\n"
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Close"]
            btn_data_row2 = ["set_echo", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            images = await MongoDB.get_data("bot_docs", "images")
            if images:
                image = random.choice(images).strip()
                await Message.send_img(chat.id, image, msg, btn)
            else:
                await Message.send_msg(chat.id, msg, btn)
        
        elif find_group:
            title = find_group.get("title")
            lang = find_group.get("lang")

            echo = find_group.get("echo")
            auto_tr = find_group.get("auto_tr")
            welcome_msg = find_group.get("welcome_msg")
            goodbye_msg = find_group.get("goodbye_msg")
            antibot = find_group.get("antibot")

            context.chat_data["edit_cname"] = "groups"
            context.chat_data["find_data"] = "chat_id"
            context.chat_data["match_data"] = chat_id
            context.chat_data["chat_id"] = chat.id
            context.chat_data["user_id"] = user.id

            msg = (
                f"<b>Chat Settings</b> -\n\n"
                f"• Title: {title}\n"
                f"• ID: <code>{chat_id}</code>\n\n"

                f"• Lang: <code>{lang}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n"
                f"• Welcome user: <code>{welcome_msg}</code>\n"
                f"• Goodbye user: <code>{goodbye_msg}</code>\n"
                f"• Antibot: <code>{antibot}</code>\n"
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Anti bot"]
            btn_data_row2 = ["set_echo", "antibot"]

            btn_name_row3 = ["Welcome", "Goodbye"]
            btn_data_row3 = ["welcome_msg", "goodbye_msg"]

            btn_name_row4 = ["Close"]
            btn_data_row4 = ["close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4)

            btn = row1 + row2 + row3 + row4

            images = await MongoDB.get_data("bot_docs", "images")
            if images:
                image = random.choice(images).strip()
                await Message.send_img(chat.id, image, msg, btn)
            else:
                await Message.send_msg(chat.id, msg, btn)

    elif chat.type in ["group", "supergroup"]:
        if user.is_bot:
            await Message.reply_msg(update, "I don't take permission from anonymous admins!")
            return

        _chk_per = await _check_permission(update, user=user)

        if not _chk_per:
            return
        
        _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
            
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

        context.chat_data["edit_cname"] = "groups"
        context.chat_data["find_data"] = "chat_id"
        context.chat_data["match_data"] = chat.id
        context.chat_data["chat_id"] = chat.id
        context.chat_data["user_id"] = user.id

        msg = (
            f"<b>Chat Settings</b> -\n\n"
            f"• Title: {title}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Welcome user: <code>{welcome_msg}</code>\n"
            f"• Goodbye user: <code>{goodbye_msg}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
        )

        btn_name_row1 = ["Language", "Auto translate"]
        btn_data_row1 = ["lang", "auto_tr"]

        btn_name_row2 = ["Echo", "Anti bot"]
        btn_data_row2 = ["set_echo", "antibot"]

        btn_name_row3 = ["Welcome", "Goodbye"]
        btn_data_row3 = ["welcome_msg", "goodbye_msg"]

        btn_name_row4 = ["Close"]
        btn_data_row4 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4)

        btn = row1 + row2 + row3 + row4

        images = await MongoDB.get_data("bot_docs", "images")
        if images:
            image = random.choice(images).strip()
            await Message.send_img(chat.id, image, msg, btn)
        else:
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
    
    msg = (
        f"Hi {user.mention_html()}! Welcome to the bot help section...\n"
        f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
        f"/start - to start the bot\n"
        f"/help - to see this message"
    )

    context.chat_data["user_id"] = user.id

    btn_name_row1 = ["Group Management", "Artificial intelligence"]
    btn_data_row1 = ["group_management", "ai"]

    btn_name_row2 = ["misc", "Bot owner"]
    btn_data_row2 = ["misc_func", "owner_func"]

    btn_name_row3 = ["Close"]
    btn_data_row3 = ["close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3)

    btn = row1 + row2 + row3
    
    images = await MongoDB.get_data("bot_docs", "images")
    if images:
        image = random.choice(images).strip()
        await Message.send_img(chat.id, image, msg, btn)
    else:
        await Message.send_msg(chat.id, msg, btn)


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
            # sleep for 2sec
            await asyncio.sleep(2)
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


async def func_bsetting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if user.id != int(owner_id):
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
    
    btn_name_row1 = ["Bot pic", "Welcome img"]
    btn_data_row1 = ["bot_pic", "welcome_img"]

    btn_name_row2 = ["Telegraph", "Images", "Lang code list"]
    btn_data_row2 = ["telegraph", "images", "lang_code_list"]

    btn_name_row3 = ["Support chat", "Server url"]
    btn_data_row3 = ["support_chat", "server_url"]

    btn_name_row4 = ["ChatGpt limit", "Imagine limit", "Usage reset"]
    btn_data_row4 = ["chatgpt_limit", "ai_imagine_limit", "usage_reset"]

    btn_name_row5 = ["Premium seller", "Premium users"]
    btn_data_row5 = ["premium_seller", "premium_users"]

    btn_name_row6 = ["⚠ Restore Settings", "Close"]
    btn_data_row6 = ["restore_db", "close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
    row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
    row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
    row6 = await Button.cbutton(btn_name_row6, btn_data_row6, True)

    btn = row1 + row2 + row3 + row4 + row5 + row6

    images = await MongoDB.get_data("bot_docs", "images")
    if images:
        image = random.choice(images).strip()
        await Message.send_img(chat.id, image, "<b>Bot Settings</b>", btn)
    else:
        await Message.send_msg(chat.id, "<b>Bot Setting</b>", btn)


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
            res = json.loads(res.text)
            for obj in res:
                service = obj.get("service")
                s_id = service.get("id")
                s_name = service.get("name")
                if s_id:
                    msg += f"<b>{s_name}</b>: <code>{s_id}</code>\n"
            
            await Message.reply_msg(update, msg)
        except Exception as e:
            logger.error(f"Error render: {e}")
            await Message.reply_msg(update, f"Error render: {e}")
    elif "restart" in msg:
        index_restart = msg.index("restart")
        service_id = msg[index_restart + len("restart"):].strip()
        
        try:
            sent_msg = await Message.reply_msg(update, "Restarting...")
            o_value = await MongoDB.get_data("bot_docs", "bot_status")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "restart")
            res = await Render.restart(service_id)
            if res.status_code != 200:
                await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "alive")
                await Message.edit_msg(update, "Failed to restart...", sent_msg)
        except Exception as e:
            logger.error(f"Error render: {e}")
            await Message.reply_msg(update, f"Error render: {e}")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "alive")
    elif "redeploy" in msg:
        index_redeploy = msg.index("redeploy")
        service_id = msg[index_redeploy + len("redeploy"):].strip()

        try:
            sent_msg = await Message.reply_msg(update, f"Redeploying...")
            o_value = await MongoDB.get_data("bot_docs", "bot_status")
            await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "restart")
            res = await Render.redeploy(service_id)
            if res.status_code != 200:
                await MongoDB.update_db("bot_docs", "bot_status", o_value, "bot_status", "alive")
                await Message.edit_msg(update, "Failed to redeploy...", sent_msg)
        except Exception as e:
            logger.error(f"Error render: {e}")
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

    if context.chat_data.get("status") == "editing":
        if msg.isdigit():
            msg = int(msg)
        context.chat_data["new_value"] = msg
        context.chat_data["status"] = ""
        return

    if chat.type == "private" and msg:
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
            return
        
        # status
        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        # Trigger
        if echo_status:
            await Message.reply_msg(update, msg)

        if auto_tr_status:
            lang_code = find_user.get("lang")
            try:
                tr_msg = translate(msg, lang_code)
            except Exception as e:
                logger.error(f"Error Translator: {e}")
                lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
                btn_name = ["Language code's"]
                btn_url = [lang_code_list]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
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
        if echo_status:
            await Message.reply_msg(update, msg)
            
        if auto_tr_status:
            lang_code = find_group.get("lang")
            try:
                tr_msg = translate(msg, lang_code)
            except Exception as e:
                logger.error(f"Error Translator: {e}")
                lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")
                btn_name = ["Language code's"]
                btn_url = [lang_code_list]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
                return
            # tanslate proccess
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg, parse_mode=ParseMode.MARKDOWN)


async def server_alive():
    server_url = await MongoDB.get_data("bot_docs", "server_url")
    bot_status = await MongoDB.get_data("bot_docs", "bot_status")
    try:
        if not bot_status or bot_status == "alive":
            await Message.send_msg(owner_id, "Bot Started!")
        elif bot_status == "restart":
            await MongoDB.update_db("bot_docs", "bot_status", bot_status, "bot_status", "alive")
            await Message.send_msg(owner_id, "Bot Restarted!")
    except Exception as e:
        logger.error(f"Error startup_msg: {e}")

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
    application.add_handler(CommandHandler("decode", func_b64decode, block=False))
    application.add_handler(CommandHandler("encode", func_b64encode, block=False))
    application.add_handler(CommandHandler("shortener", func_shortener, block=False))
    application.add_handler(CommandHandler("ping", func_ping, block=False))
    application.add_handler(CommandHandler("calc", func_calc, block=False))
    application.add_handler(CommandHandler("webshot", func_webshot, block=False))
    application.add_handler(CommandHandler("weather", func_weather, block=False))
    application.add_handler(CommandHandler("imagine", func_imagine, block=False))
    application.add_handler(CommandHandler("gpt", func_chatgpt, block=False))
    application.add_handler(CommandHandler("ytdl", func_ytdl, block=False))
    application.add_handler(CommandHandler("yts", func_yts, block=False))
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
    application.add_handler(CommandHandler("lock", func_lockchat, block=False))
    application.add_handler(CommandHandler("unlock", func_unlockchat, block=False))
    application.add_handler(CommandHandler("adminlist", func_adminlist, block=False))
    application.add_handler(CommandHandler("help", func_help, block=False))
    # owner
    application.add_handler(CommandHandler("broadcast", func_broadcast, block=False))
    application.add_handler(CommandHandler("database", func_database, block=False))
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
    #Thread(target=start_up_work).start()

    async def start_up_work():
        await update_database()
        await server_alive()
    
    loop = asyncio.get_event_loop()
    loop.create_task(start_up_work())
    loop.create_task(main())
    loop.run_forever()
