import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


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
            images = LOCAL_DATABASE.get_data("bot_docs", "images")
            if not images:
                images = await MongoDB.get_data("bot_docs", "images")
            
            if images:
                image = random.choice(images).strip()
            else:
                image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
                if not image:
                    image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(user.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
                if not image:
                    image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(user.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(user.id, msg, btn)
        
        find_user = await LOCAL_DATABASE.find_one("users", user.id)
        if not find_user:
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

            await MongoDB.insert_single_data("users", data)
            await LOCAL_DATABASE.insert_data("users", user.id, data)
        
        if chat.type != "private":
            _bot_info = await bot.get_me()
            await Message.reply_msg(update, f"Sent in your pm! <a href='http://t.me/{_bot_info.username}'>Check</a>")

    except Forbidden:
        _bot_info = await bot.get_me()
        await Message.reply_msg(update, f"Hola, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
        
    except Exception as e:
        logger.error(e)
