import os
from alive import alive

alive()
import requests
import asyncio
import pymongo
import logging, telegram
from typing import Optional, Tuple
from base64 import b64decode, b64encode
from deep_translator import GoogleTranslator
from telegram import Chat, ChatMember, ChatMemberUpdated, Update as update, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (Application, ChatMemberHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CallbackContext)

# config
bot_token = os.environ['bot_token']
bot_log = os.environ['bot_log']
activity_log_channel = os.environ['activity_log_channel']
shrinkme_api_key = os.environ['shrinkme_api_key']
mongodb_uri = os.environ['mongodb_uri']
ping_url = "https://ping-pong.bishalqx980.repl.co/"
ownerID = 2134776547

# mongodb
client = pymongo.MongoClient(mongodb_uri)
mongodb = client["melina_db"]
melina_dbdata = mongodb["melina"]
users_dbdata = mongodb["users"]
groups_dbdata = mongodb["groups"]
channels_dbdata = mongodb["channels"]

bot = telegram.Bot(token=bot_token)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user = update.effective_user
  collection_melina = melina_dbdata.find_one({})
  avatar = collection_melina.get("avatar")

  #message = await update.effective_message.reply_text("⌛")
  #await asyncio.sleep(2.8)
  #await message.delete()
  welcome_text = (
    f"Hi, {user.mention_html()} !! I'm <a href='https://t.me/YmlzaGFsbot'>Melina</a>!\n"
    f"⪧ I can convert base64 to text.\n"
    f"⪧ I can short any URL.\n"
    f"⪧ I can translate any language to English.\n"
    f"⪧ I can log Group user join left /setlog for more details.\n"
    f"⪧ Bot Config Menu /config for more feature\n"
    f"🆘 To-do: Add more feature!\n\n"
    f"♯ 🛠 This bot has many HIDDEN Feature's which are only available for Developer!!\n\n"
    f"♯ 🖥 Coded & Developed by @bishalqx980 ⩆ @bishalqx680\n\n‧̍̊·̊‧̥°̩̥˚̩̩̥͙°̩̥‧̥·̊‧̍̊ ♡ °̩̥˚̩̩̥͙°̩̥ ·͙*̩̩͙˚̩̥̩̥*̩̩̥͙·̩̩̥͙*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ °̩̥˚̩̩̥͙°̩̥ ♡ ‧̍̊·̊‧̥°̩̥˚̩̩̥͙°̩̥‧̥·̊‧̍̊"
  )
  welcome_keyboard = [
    [
      InlineKeyboardButton("Developer 👨‍💻", url="https://t.me/bishalqx980"),
      InlineKeyboardButton("Source 📖", url="https://telegra.ph/Melina---httpstmeYmlzaGFsbot-12-03")
    ],
    [
      InlineKeyboardButton("Melina Updates ⚡", url="https://t.me/MelinaUpdates"),
    ],
    [
      InlineKeyboardButton("About ℹ", callback_data="about"),
      InlineKeyboardButton("Help ❓", callback_data="help")
    ]
  ]
  welcome_reply_markup = InlineKeyboardMarkup(welcome_keyboard)

  await update.message.reply_photo(photo=avatar, caption=welcome_text, parse_mode=ParseMode.HTML, reply_markup=welcome_reply_markup)

  user_info = {
    "user_id": user.id,
    "user_name": user.full_name,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "user_mention": user.mention_html(),
    "user_username": user.username,
    "user_lang_code": user.language_code
  }

  check_user = users_dbdata.find_one({'user_id': user_info['user_id']})
  if check_user:
    print("User already exists in the database")
    return
  users_dbdata.insert_one(user_info)

async def button(update: Update, context: CallbackContext) -> None:
  effective_chat = update.effective_chat
  query = update.callback_query
  await query.answer()

  welcome_text = (
    f"Damn, Welcome back Darling !! Can you remember me? I'm <a href='https://t.me/YmlzaGFsbot'>Melina</a>!\n"
    f"⪧ I can convert base64 to text.\n"
    f"⪧ I can short any URL.\n"
    f"⪧ I can translate any language to English.\n"
    f"⪧ I can log Group user join left /setlog for more details.\n"
    f"⪧ Bot Config Menu /config for more feature\n"
    f"🆘 To-do: Add more feature!\n\n"
    f"♯ 🛠 This bot has many HIDDEN Feature's which are only available for Developer!!\n\n"
    f"♯ 🖥 Coded & Developed by @bishalqx980 ⩆ @bishalqx680\n\n‧̍̊·̊‧̥°̩̥˚̩̩̥͙°̩̥‧̥·̊‧̍̊ ♡ °̩̥˚̩̩̥͙°̩̥ ·͙*̩̩͙˚̩̥̩̥*̩̩̥͙·̩̩̥͙*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ °̩̥˚̩̩̥͙°̩̥ ♡ ‧̍̊·̊‧̥°̩̥˚̩̩̥͙°̩̥‧̥·̊‧̍̊"
  )
  welcome_keyboard = [
    [
      InlineKeyboardButton("Developer 👨‍💻", url="https://t.me/bishalqx980"),
      InlineKeyboardButton("Source 📖", url="https://telegra.ph/Melina---httpstmeYmlzaGFsbot-12-03")
    ],
    [
      InlineKeyboardButton("Melina Updates ⚡", url="https://t.me/MelinaUpdates"),
    ],
    [
      InlineKeyboardButton("About ℹ", callback_data="about"),
      InlineKeyboardButton("Help ❓", callback_data="help")
    ]
  ]
  welcome_reply_markup = InlineKeyboardMarkup(welcome_keyboard)

  about_text = (
    f"---⊱ ABOUT ⊰---\n"
    f"┏━━━━━━━━━━━━━\n"
    f"◈ Lang: Python 3.11\n"
    f"◈ Database: MongoDB\n"
    f"◈ Hosted on: VPS\n"
    f"◈ Version: UltimateX ⫗\n-----(03-Nov-2023)\n"
    f"◈ Online Since: 29-April-2023\n"
    f"◈ Last Updated: 15-Dec-2023\n"
    f"┗━━━━━━━━━━━━━\n\n"
  )

  help_text = (
    f"▣ /id - Show chat ID\n"
    f"▣ /info - Show user info\n"
    f"▣ /ping - Check server status\n"
    f"▣ /setlog - Set log for a Chat\n"
    f"▣ /config - Bot config menu\n"
    f"▣ /help - get help\n\n"
    f"⚠ Owner Only\n"
    f"▣ /stats - 📊\n"
    f"▣ /broadcast - 📢"
  )
  
  main_menu_keyboard = [
    [
      InlineKeyboardButton("Developer 👨‍💻", url="https://t.me/bishalqx980"),
      InlineKeyboardButton("Source 📖", url="https://telegra.ph/Melina---httpstmeYmlzaGFsbot-12-03")
    ],
    [
      InlineKeyboardButton("Melina Updates ⚡", url="https://t.me/MelinaUpdates"),
    ],
    [
      InlineKeyboardButton("About ℹ", callback_data="about"),
      InlineKeyboardButton("Help ❓", callback_data="help")
    ],
    [
      InlineKeyboardButton("↻ Main Menu", callback_data="main_menu")
    ]
  ]

  main_menu_reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

  url_data = {
    "delete_url_status": "✅"
  }
  url_data2 = {
    "delete_url_status": "❌"
  }
  tgurl_data = {
    "delete_tgurl_status": "✅"
  }
  tgurl_data2 = {
    "delete_tgurl_status": "❌"
  }
  delete_admin_cmd_data = {
    "delete_admin_cmd_status": "✅"
  }
  delete_admin_cmd_data2 = {
    "delete_admin_cmd_status": "❌"
  }
  translator_data = {
    "translator_status": "✅"
  }
  translator_data2 = {
    "translator_status": "❌"
  }
  short_url_data = {
    "short_url_status": "✅"
  }
  short_url_data2 = {
    "short_url_status": "❌"
  }
  base64_data = {
    "base64_status": "✅"
  }
  base64_data2 = {
    "base64_status": "❌"
  }

  group_config_keyboard = [
    [
      InlineKeyboardButton("🗑 All Links", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_url"),
      InlineKeyboardButton("❌", callback_data="delete_url_no")
    ],
    [
      InlineKeyboardButton("🗑 Mentions", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_tgurl"),
      InlineKeyboardButton("❌", callback_data="delete_tgurl_no")
    ],
    [
      InlineKeyboardButton("🗑 Admin cmds", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_admin_cmd"),
      InlineKeyboardButton("❌", callback_data="delete_admin_cmd_no")
    ],
    [
      InlineKeyboardButton("Lang Translator", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="translator"),
      InlineKeyboardButton("❌", callback_data="translator_no")
    ],
    [
      InlineKeyboardButton("ShortURL Convert", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="short_url"),
      InlineKeyboardButton("❌", callback_data="short_url_no")
    ],
    [
      InlineKeyboardButton("Base64 Convert", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="base64"),
      InlineKeyboardButton("❌", callback_data="base64_no")
    ],
    [
      InlineKeyboardButton("⨯ Close ⨯", callback_data="close")
    ]
  ]
  group_config_reply_markup = InlineKeyboardMarkup(group_config_keyboard)

  async def update_mongodb_data(status):
    collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_groups_dbdata:
      groups_dbdata.update_one({"chat_id": effective_chat.id},{"$set": status})
    else:
      await update.message.reply_text(f"<b>⚠ Remove ME from this Group & Add again in Group as admin!\nThen Try again!</b>", parse_mode=ParseMode.HTML)

  if query.data == "about":
    await query.message.edit_caption(about_text, parse_mode=ParseMode.HTML, reply_markup=main_menu_reply_markup)
  elif query.data == "help":
    await query.message.edit_caption(help_text, parse_mode=ParseMode.HTML, reply_markup=main_menu_reply_markup)
  elif query.data == "main_menu":
    await query.message.edit_caption(welcome_text, parse_mode=ParseMode.HTML, reply_markup=welcome_reply_markup)

  if query.data == "delete_url" or query.data == "delete_url_no" or query.data == "delete_tgurl" or query.data == "delete_tgurl_no" or query.data == "delete_admin_cmd" or query.data == "delete_admin_cmd_no" or query.data == "translator" or query.data == "translator_no" or query.data == "short_url" or query.data == "short_url_no" or query.data == "base64" or query.data == "base64_no":
    if query.data == "delete_url":
      await update_mongodb_data(url_data)
    elif query.data == "delete_url_no":
      await update_mongodb_data(url_data2)
    elif query.data == "delete_tgurl":
      await update_mongodb_data(tgurl_data)
    elif query.data == "delete_tgurl_no":
      await update_mongodb_data(tgurl_data2)
    elif query.data == "delete_admin_cmd":
      await update_mongodb_data(delete_admin_cmd_data)
    elif query.data == "delete_admin_cmd_no":
      await update_mongodb_data(delete_admin_cmd_data2)
    elif query.data == "translator":
      await update_mongodb_data(translator_data)
    elif query.data == "translator_no":
      await update_mongodb_data(translator_data2)
    elif query.data == "short_url":
      await update_mongodb_data(short_url_data)
    elif query.data == "short_url_no":
      await update_mongodb_data(short_url_data2)
    elif query.data == "base64":
      await update_mongodb_data(base64_data)
    elif query.data == "base64_no":
      await update_mongodb_data(base64_data2)
      
    collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_groups_dbdata:
      delete_url_status = collection_groups_dbdata.get("delete_url_status")
      delete_tgurl_status = collection_groups_dbdata.get("delete_tgurl_status")
      delete_admin_cmd_status = collection_groups_dbdata.get("delete_admin_cmd_status")
      translator_status = collection_groups_dbdata.get("translator_status")
      short_url_status = collection_groups_dbdata.get("short_url_status")
      base64_status = collection_groups_dbdata.get("base64_status")
    else:
      delete_url_status = "❌"
      delete_tgurl_status = "❌"
      delete_admin_cmd_status = "❌"
      translator_status = "❌"
      short_url_status = "❌"
      base64_status = "❌"
    config_text = (
      f"<b>⪧ Group Config Menu (BETA) ⪦</b>\n\n"
      f"▣ Config of {effective_chat.title}\n"
      f"◦ 🗑 All Links: {delete_url_status}\n"
      f"◦ 🗑 Mentions (@username): {delete_tgurl_status}\n"
      f"◦ 🗑 Admin cmds: {delete_admin_cmd_status}\n"
      f"◦ Lang Translator: {translator_status}\n"
      f"◦ ShortURL Convert: {short_url_status}\n"
      f"◦ Base64 Convert: {base64_status}\n\n"
      f"Note: <i>✅ means Enabled & ❌ means Disabled!</i>"
    )

    await query.message.edit_text(config_text, parse_mode=ParseMode.HTML, reply_markup=group_config_reply_markup)

  elif query.data == "close":
    await query.message.delete()
    await query.message.reply_to_message.delete()

async def chatID(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  effective_chat = update.effective_chat

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  if update.message.reply_to_message:
    user_id = update.message.reply_to_message.from_user.id
  else:
    user_id = update.message.from_user.id

  chat_id = update.message.chat_id
  if chat_type == "Group":
    await update.effective_message.reply_text(
      f"<b>◈ UserID: </b><code>{user_id}</code>\n"
      f"<b>◈ ChatID: </b><code>{chat_id}</code>",
      parse_mode=ParseMode.HTML,
      disable_web_page_preview=True
    )
  else:
    await update.effective_message.reply_text(
      f"<b>◈ UserID: </b><code>{user_id}</code>",
      parse_mode=ParseMode.HTML,
      disable_web_page_preview=True
    )
  
async def info(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_info = update.effective_user
  message = update.message
  # User attributes
  if message.reply_to_message:
    replied_message = message.reply_to_message
    message_id = message.reply_to_message.message_id
    user_id = replied_message.from_user.id
    user_name = replied_message.from_user.full_name
    first_name = replied_message.from_user.first_name
    last_name = replied_message.from_user.last_name
    user_mention = replied_message.from_user.mention_html()
    user_username = replied_message.from_user.username
    user_lang_code = replied_message.from_user.language_code
  else:
    message_id = message.message_id
    user_id = user_info.id
    user_name = user_info.full_name
    first_name = user_info.first_name
    last_name = user_info.last_name
    user_mention = user_info.mention_html()
    user_username = user_info.username
    user_lang_code = user_info.language_code
    
  message_text = (
    f"<b>◈ Name:</b> {user_name}\n"
    f"<b>◦ Firstname:</b> {first_name}\n"
    f"<b>◦ Lastname:</b> {last_name}\n"
    f"<b>◈ UserID:</b> <code>{user_id}</code>\n"
    f"<b>◈ Mention:</b> {user_mention}\n"
    f"<b>◈ Username:</b> @{user_username}\n"
    f"<b>◈ Language Code:</b> {user_lang_code}\n\n"
    f"⪧ <i>info generator beta</i>"
  )
  await update.effective_message.reply_text(
    message_text,
    parse_mode=ParseMode.HTML,
    reply_to_message_id=message_id,
    disable_web_page_preview=True
  )

async def ping(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  message = update.message
  text = await message.reply_text(f"Pinging...")
  try:
    response = requests.get(ping_url)
    if response.status_code == 200:
      ping_time = response.elapsed.total_seconds() * 1000
      ping_time = round(ping_time, 2)
      await text.edit_text(f"↻ Server respond in {ping_time}ms", parse_mode=ParseMode.HTML)
    else:
      await text.edit_text(f"Server took so long to response 💻")
  except requests.RequestException as e:
    await text.edit_text(f"Error: {e}")

async def help(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  text = (
    f"▣ /id - Show chat ID\n"
    f"▣ /info - Show user info\n"
    f"▣ /ping - Check server status\n"
    f"▣ /setlog - Set log for a Chat\n"
    f"▣ /config - Bot config menu\n"
    f"▣ /help - get help\n\n❗ /start me if you are lost!\n\n"
    f"⚠ Owner Only\n"
    f"▣ /stats - 📊\n"
    f"▣ /broadcast - 📢"
  )
  await update.message.reply_text(text)

# ---------------------------- owner only -------------------------------------------------
async def stats(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  total_channels_count = channels_dbdata.count_documents({})
  total_groups_count = groups_dbdata.count_documents({})
  total_users_count = users_dbdata.count_documents({})

  if update.effective_message.from_user.id == ownerID:
    await update.message.reply_text(f"Total Channels: {total_channels_count}\nTotal Groups: {total_groups_count}\nTotal Users: {total_users_count}", parse_mode=ParseMode.HTML)
  else:
    deny = await update.message.reply_text("❌")
    await asyncio.sleep(3)
    await deny.delete()

async def broadcast(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  total_users_count = users_dbdata.count_documents({})
  effective_message = update.effective_message
  message = update.message

  if effective_message.from_user.id == ownerID:
    if not message.reply_to_message:
      text = "⚠ Reply to the message which you want to broadcast!"
      await update.message.reply_text(text)
      return
    else:
      text = message.reply_to_message.text

    count = 0

    user_ids = users_dbdata.find({})
    to_send_chat_ids = []
    for user_id in user_ids:
      user_id_list = user_id.get('user_id')
      to_send_chat_ids.append(user_id_list)
    for chat_id in to_send_chat_ids:
      try:
        await bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
        count += 1
      except telegram.error.Forbidden as e:
        print(e)
    await bot.sendMessage(chat_id=ownerID, text=f"Broadcast Message sent to: {count}/{total_users_count}")
  else:
    deny = await update.message.reply_text("❌")
    await asyncio.sleep(3)
    await deny.delete()


# ------------------------------------------ Filter ------------------------------------------
async def filterText(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  effective_chat = update.effective_chat
  effective_user = update.effective_user
  effective_message = update.effective_message
  message = update.message

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  if message and message.reply_to_message:
    message_id = message.reply_to_message.message_id
  elif message:
    message_id = message.message_id
  else:
    pass

  collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
  if collection_groups_dbdata:
    delete_url_status = collection_groups_dbdata.get("delete_url_status")
    delete_tgurl_status = collection_groups_dbdata.get("delete_tgurl_status")
    delete_admin_cmd_status = collection_groups_dbdata.get("delete_admin_cmd_status")
    translator_status = collection_groups_dbdata.get("translator_status")
    short_url_status = collection_groups_dbdata.get("short_url_status")
    base64_status = collection_groups_dbdata.get("base64_status")
  else:
    delete_url_status = "❌"
    delete_tgurl_status = "❌"
    delete_admin_cmd_status = "❌"
    translator_status = "❌"
    short_url_status = "❌"
    base64_status = "❌"
  
  baseMessage = effective_message.text
  decoded_text = ""
  
  if effective_chat.type == Chat.CHANNEL and effective_message.text == "/setlog":
    await bot.sendMessage(chat_id=effective_chat.id, text=f"Now forward the <code>/setlog</code> command to the chat you wish to log here.", parse_mode=ParseMode.HTML, reply_to_message_id=effective_message.message_id)
  else:
    pass

  # message deleter

  normal_links = ["http://", "https://"]
  telegram_links = ["@"]
  melina = ["Melina", "Darling", "melina", "darling"]

  if effective_message.from_user and effective_message.text:
    if effective_message.text.startswith('!') or effective_message.text.startswith('/'):
      if effective_message.from_user.id == ownerID:
        await effective_message.delete()
      elif chat_type == "Group" and delete_admin_cmd_status == "✅":
        chatmember = await effective_chat.get_member(effective_user.id)
        if chatmember.status in ["creator", "administrator"]:
          await effective_message.delete()
        else:
          pass
      else:
        pass
    elif delete_url_status == "✅" and any(word in effective_message.text for word in normal_links):
      await effective_message.delete()
    elif delete_tgurl_status == "✅" and any(word in effective_message.text for word in telegram_links):
      await effective_message.delete()
    else:
      pass
  else:
    pass

  # translator

  if message and not effective_message.text.startswith('/'):
    translator = GoogleTranslator(source='auto', target='en')
    translated_text = translator.translate(message.text)
    if translated_text != message.text and translated_text != None:
      if chat_type == "Group" and translator_status == "✅":
        await update.message.reply_text(f"{translated_text}", parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
      elif chat_type == "Private":
        await update.message.reply_text(f"{translated_text}", parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
      else:
        pass
    else:
      pass
  else:
    pass

  # shortener url

  if any(word in effective_message.text for word in normal_links):
    try:
      api_url = f'https://shrinkme.io/api?api={shrinkme_api_key}&url={baseMessage}'
      response = requests.get(api_url)
      shortened_url = response.json().get("shortenedUrl")
  
      if shortened_url != "":
        if chat_type == "Group" and short_url_status == "✅":
          await bot.send_message(
            chat_id=effective_chat.id,
            text=f"<b>◈ Base URL\n◜\n<code>{baseMessage}</code>\n◟\n◈ Shortener URL\n◜\n<code>{shortened_url}</code>\n◟</b>",
            parse_mode=ParseMode.HTML,
            reply_to_message_id=message_id,
            disable_web_page_preview=True
          )
        elif chat_type == "Private":
          await bot.send_message(
            chat_id=effective_chat.id,
            text=f"<b>◈ Base URL\n◜\n<code>{baseMessage}</code>\n◟\n◈ Shortener URL\n◜\n<code>{shortened_url}</code>\n◟</b>",
            parse_mode=ParseMode.HTML,
            reply_to_message_id=message_id,
            disable_web_page_preview=True
          )
        else:
          pass
      else:
        pass
    except Exception as e:
      logging.error(f"Error: {e}")
  else:
    pass

  # base64

  if effective_message.text:
    if chat_type == "Group" and base64_status == "✅":
      try:
        decoded_text = b64decode(baseMessage).decode('utf-8')
        encoded_text = b64encode(decoded_text.encode('utf-8')).decode('utf-8')
        if encoded_text == baseMessage and encoded_text != "":
          message_text = (
            f"<b>◈ Base Text (base64)\n◜\n<code>{baseMessage}</code>\n◟\n"
            f"◈ Decoded Text\n◜\n<code>{decoded_text}</code>\n◟</b>"
          )
          await update.message.reply_text(message_text, parse_mode=ParseMode.HTML, reply_to_message_id=message_id, disable_web_page_preview=True)
        else:
          pass
      except Exception as e:
        print(e)
    elif chat_type == "Private":
      decoded_text = ""
      lines = baseMessage.split("\n")
      for line in lines:
        try:
          decoded_line = b64decode(line).decode("utf-8")
          decoded_text += f"<code>{decoded_line}</code>" + "\n"
        except:
          decoded_text += f"<b>⪧ {line}</b>" + "\n"
      await update.message.reply_text(f"<b>◈ Decoded Text</b>\n◜\n{decoded_text}◟", parse_mode=ParseMode.HTML, reply_to_message_id=message_id, disable_web_page_preview=True)
    else:
      pass
  else:
    pass

  # Melina Hi

  if effective_message.text and any(word in effective_message.text for word in melina):
    if effective_message.from_user.id == ownerID:
      await effective_message.reply_text(f"I'm here Boss!", parse_mode=ParseMode.HTML, reply_to_message_id=message_id)
    else:
      await effective_message.reply_text(f"How can I help you, {effective_user.mention_html()}?\n/start - To know what can I do.", parse_mode=ParseMode.HTML, reply_to_message_id=message_id)
  else:
    pass

async def filterCaption(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  effective_chat = update.effective_chat
  message = update.message

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
  if collection_groups_dbdata:
    translator_status = collection_groups_dbdata.get("translator_status")
  else:
    translator_status = "❌"


  if message:
    translator = GoogleTranslator(source='auto', target='en')
    if message.caption:
      translated_caption = translator.translate(message.caption)
    else:
      translated_caption = "No caption found!"
    if translated_caption != message.caption and translated_caption != None:
      if chat_type == "Group" and translator_status == "✅":
        await update.message.reply_text(f"{translated_caption}", parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
      elif chat_type == "Private":
        await update.message.reply_text(f"{translated_caption}", parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
      else:
        pass
    else:
      pass
  else:
    pass

async def config(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  effective_chat = update.effective_chat
  effective_user = update.effective_user

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  if chat_type == "Group":
    chatmember = await effective_chat.get_member(effective_user.id)
    if chatmember.status not in ["creator", "administrator"]:
      error_message = await update.message.reply_text(f"<b>❌ Only group admins can use this command.</b>", parse_mode=ParseMode.HTML)
      await asyncio.sleep(5)
      await error_message.delete()
      return
    collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_groups_dbdata:
      delete_url_status = collection_groups_dbdata.get("delete_url_status")
      delete_tgurl_status = collection_groups_dbdata.get("delete_tgurl_status")
      delete_admin_cmd_status = collection_groups_dbdata.get("delete_admin_cmd_status")
      translator_status = collection_groups_dbdata.get("translator_status")
      short_url_status = collection_groups_dbdata.get("short_url_status")
      base64_status = collection_groups_dbdata.get("base64_status")
    else:
      delete_url_status = "❌"
      delete_tgurl_status = "❌"
      delete_admin_cmd_status = "❌"
      translator_status = "❌"
      short_url_status = "❌"
      base64_status = "❌"
  else:
    await update.message.reply_text(f"<b>⚠ This command made for Group's only!</b>", parse_mode=ParseMode.HTML)

  text = (
    f"<b>⪧ Group Config Menu (BETA) ⪦</b>\n\n"
    f"▣ Config of {effective_chat.title}\n"
    f"◦ 🗑 All Links: {delete_url_status}\n"
    f"◦ 🗑 Mentions (@username): {delete_tgurl_status}\n"
    f"◦ 🗑 Admin cmds: {delete_admin_cmd_status}\n"
    f"◦ Lang Translator: {translator_status}\n"
    f"◦ ShortURL Convert: {short_url_status}\n"
    f"◦ Base64 Convert: {base64_status}\n\n"
    f"Note: <i>✅ means Enabled & ❌ means Disabled!</i>"
  )
  group_config_keyboard = [
    [
      InlineKeyboardButton("🗑 All Links", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_url"),
      InlineKeyboardButton("❌", callback_data="delete_url_no")
    ],
    [
      InlineKeyboardButton("🗑 Mentions", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_tgurl"),
      InlineKeyboardButton("❌", callback_data="delete_tgurl_no")
    ],
    [
      InlineKeyboardButton("🗑 Admin cmds", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="delete_admin_cmd"),
      InlineKeyboardButton("❌", callback_data="delete_admin_cmd_no")
    ],
    [
      InlineKeyboardButton("Lang Translator", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="translator"),
      InlineKeyboardButton("❌", callback_data="translator_no")
    ],
    [
      InlineKeyboardButton("ShortURL Convert", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="short_url"),
      InlineKeyboardButton("❌", callback_data="short_url_no")
    ],
    [
      InlineKeyboardButton("Base64 Convert", callback_data="none"),
      InlineKeyboardButton("✅", callback_data="base64"),
      InlineKeyboardButton("❌", callback_data="base64_no")
    ],
    [
      InlineKeyboardButton("⨯ Close ⨯", callback_data="close")
    ]
  ]
  group_config_reply_markup = InlineKeyboardMarkup(group_config_keyboard)

  await update.message.reply_text(f"{text}", parse_mode=ParseMode.HTML, reply_markup=group_config_reply_markup)

# Other -------------------------------------------------------------------------------------------------------------------------------------------

async def set_log(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  effective_chat = update.effective_chat
  effective_user = update.effective_user
  forward_from_chat = update.message.forward_from_chat

  if not forward_from_chat:
    text = (
      f"<b>You can setup log by using /setlog command in a channel</b>\n"
      f"⩺ Steps:\n"
      f"1. Add this bot to a channel where you want to log user join/left then add this in your group as admin which group you want to track!\n"
      f"2. Goto that channel and type /setlog then forward the /setlog command from channel to your Group!\n"
      f"🎉 Setup DONE ✨\n- <i>From now bot will log your group user join/left in channel!</i>"
    )
    error_message = await update.message.reply_text(f"{text}", parse_mode=ParseMode.HTML)
    return
  
  chatmember = await effective_chat.get_member(effective_user.id)
  if chatmember.status not in ["creator", "administrator"]:
    error_message = await update.message.reply_text(f"<b>❌ Only group admins can use this command.</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(5)
    await error_message.delete()
    return

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  chat_title = effective_chat.title
  log_channel_title = forward_from_chat.title
  log_channel_id = forward_from_chat.id

  data = {
    "log_channel_title": log_channel_title,
    "log_channel_id": log_channel_id
  }
  
  if chat_type == "Group" and forward_from_chat.type == Chat.CHANNEL:
    await update.message.delete()
    message = f"\n⩶⩶⩶⩶⩶⩶⩶⩶⩶⩶\n<b>⪧ Group: </b>{chat_title}\n<b>⪧ Log Channel: </b>{log_channel_title}"
    collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_groups_dbdata:
      groups_dbdata.update_one({"chat_id": effective_chat.id}, {'$set': data})
      await bot.sendMessage(chat_id=log_channel_id, text=f"<b>✅ Log Channel Updated:</b>{message}", parse_mode=ParseMode.HTML)
    else:
      await update.message.reply_text(f"<b>⚠ Remove ME from this Group & Add again in Group as admin!\nThen Try again!</b>", parse_mode=ParseMode.HTML)
  else:
    error_message = await update.message.reply_text(f"<b>❌ This command only made for Channel use.</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(5)
    await error_message.delete()


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
  status_change = chat_member_update.difference().get("status")
  old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

  if status_change is None:
    return None

  old_status, new_status = status_change
  was_member = old_status in [
    ChatMember.MEMBER,
    ChatMember.OWNER,
    ChatMember.ADMINISTRATOR,
  ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
  is_member = new_status in [
    ChatMember.MEMBER,
    ChatMember.OWNER,
    ChatMember.ADMINISTRATOR,
  ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

  return was_member, is_member


async def member_status(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  result = extract_status_change(update.chat_member)
  if result is None:
    return
  was_member, is_member = result
  member_name = update.chat_member.new_chat_member.user.mention_html()
  chat = update.effective_chat
  user_id = update.effective_user.id
  member = await bot.get_chat_member_count(chat.id)
  commontxt = (
    f"{chat.title}\n\n◈ ChatID: <code>{chat.id}</code>\n"
    f"◈ Name: {member_name}\n"
    f"◈ UserID: <code>{user_id}</code>\n"
    f"◈ T-Member: {member}\n\n"
    f"@YmlzaGFsbot ◊ beta log generator</b>"
  )
  member_join_text = f"<b>🟢 {commontxt}"
  member_left_text = f"<b>🔴 {commontxt}"

  findchatid = groups_dbdata.find_one({"chat_id": chat.id})
  log_channel_id = findchatid.get("log_channel_id")

  if not was_member and is_member:
    await bot.send_message(chat_id=log_channel_id, text=member_join_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
  elif was_member and not is_member:
    await bot.send_message(chat_id=log_channel_id, text=member_left_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def bot_status(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  result = extract_status_change(update.my_chat_member)
  if result is None:
    return
  was_member, is_member = result
  effective_user = update.effective_user
  effective_chat = update.effective_chat

  Pctxt = (
    f"\n\n◈ Name : {effective_user.mention_html()}\n"
    f"◈ ID   : <code>{effective_user.id}</code>\n\n"
    f"@YmlzaGFsbot</b>"
  )
  Gctxt = (
    f"\n\n◈ Group Name: <b>{effective_chat.title}\n"
    f"◈ ChatID: <code>{effective_chat.id}</code>\n"
    f"◈ Name: {effective_user.mention_html()}\n"
    f"◈ ID: <code>{effective_user.id}</code>\n\n"
    f"@YmlzaGFsbot</b>"
  )
  Cctxt = (
      f"\n\n◈ Channel Name: {effective_chat.title}\n"
      f"◈ ChatID: <code>{effective_chat.id}</code>\n"
      f"◈ Name: {effective_user.mention_html()}\n"
      f"◈ ID: <code>{effective_user.id}</code>\n\n"
      f"@YmlzaGFsbot</b>"
  )

  if effective_chat.type == Chat.PRIVATE:
    chat_type = "Private"
  elif effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
    chat_type = "Group"
  elif effective_chat.type == Chat.CHANNEL:
    chat_type = "Channel"

  added_by = effective_user.mention_html()
  chat_title = effective_chat.title
  chat_id = effective_chat.id

  data = {
    "chat_type": chat_type,
    "added_by": added_by,
    "chat_title": chat_title,
    "chat_id": chat_id
  }

  if chat_type == "Group":
    collection_groups_dbdata = groups_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_groups_dbdata:
      groups_dbdata.update_one({"chat_id": effective_chat.id},{"$set": data})
    else:
      groups_dbdata.insert_one(data)
  elif chat_type == "Channel":
    collection_channels_dbdata = channels_dbdata.find_one({"chat_id": effective_chat.id})
    if collection_channels_dbdata:
      channels_dbdata.update_one({"chat_id": effective_chat.id},{"$set": data})
    else:
      channels_dbdata.insert_one(data)
  else:
    pass

  return
  if was_member and not is_member:
    await bot.send_message(text=f"<b>🤖 Has been Removed from a Group ❌ {Gctxt}",chat_id=activity_log_channel, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


  if chat_type == "Private":
    if not was_member and is_member:
      await bot.send_message(text=f"<b>🤖 Has been Unblocked by ✅ {Pctxt}", chat_id=activity_log_channel, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif was_member and not is_member:
      await bot.send_message(text=f"<b>🤖 Has been Blocked by ❌ {Pctxt}", chat_id=activity_log_channel, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

  elif not was_member and is_member:
    await bot.send_message(text=f"<b>🤖 Has been Added to a Channel ✅ {Cctxt}", chat_id=activity_log_channel, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
  elif was_member and not is_member:
    await bot.send_message(text=f"<b>🤖 Has been Removed from a Channel ❌ {Cctxt}", chat_id=activity_log_channel, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def caption(update, context: ContextTypes.DEFAULT_TYPE) -> None:
  caption = update.message.caption
  await update.message.reply_text(f"Caption: {caption}")


def main() -> None:
  # Create the Application and pass it your bot's token.
  application = Application.builder().token(bot_token).build()

  # Handle members joining/leaving chats.
  application.add_handler(ChatMemberHandler(bot_status, ChatMemberHandler.MY_CHAT_MEMBER))
  application.add_handler(ChatMemberHandler(member_status, ChatMemberHandler.CHAT_MEMBER))

  # Start the bot
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button))

  # Show chat ID
  application.add_handler(CommandHandler("id", chatID))

  # Show info
  application.add_handler(CommandHandler("info", info))

  # ping
  application.add_handler(CommandHandler("ping", ping))

  # help
  application.add_handler(CommandHandler("help", help))

  # owner only
  application.add_handler(CommandHandler("stats", stats))
  application.add_handler(CommandHandler("broadcast", broadcast))

  # set log
  application.add_handler(CommandHandler("setlog", set_log))

  # Config
  application.add_handler(CommandHandler("config", config))

  # base64 & Agent
  application.add_handler(MessageHandler(filters.TEXT, filterText))
  application.add_handler(MessageHandler(filters.CAPTION, filterCaption))

  # Run the bot until the user presses Ctrl-C
  # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
  # To reset this, simply pass `allowed_updates=[]`
  application.run_polling(allowed_updates=update.ALL_TYPES)


if __name__ == "__main__":
  main()