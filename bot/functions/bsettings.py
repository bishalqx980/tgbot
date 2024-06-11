import random
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.power_users import _power_users


async def func_bsettings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    _bot = await LOCAL_DATABASE.find("bot_docs")
    if not _bot:
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        if not _bot:
            logger.error("_bot not found in db...")
            return
        await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)
    
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "bot_docs",
        "db_find ": "_id",
        "db_vlaue": _bot.get("_id"),
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer": None
    }

    await LOCAL_DATABASE.insert_data("data_center", chat.id, data)
    
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

    images = await LOCAL_DATABASE.get_data("bot_docs", "images")
    if not images:
        images = await MongoDB.get_data("bot_docs", "images")
    
    if images:
        image = random.choice(images).strip()
    else:
        image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
        if not image:
            image = await MongoDB.get_data("bot_docs", "bot_pic")
    
    if image:
        await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
    else:
        await Message.send_msg(chat.id, "<u><b>Bot Settings</b></u>", btn)
