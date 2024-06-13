import random
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.all_db_search import all_db_search
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

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
        "collection_name": None,
        "db_find ": None,
        "db_vlaue": None,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer": None
    }

    await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

    if chat.type == "private":
        db = await all_db_search("users", "user_id", user.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return
        
        find_user = db[1]
        
        user_mention = find_user.get("mention")
        lang = find_user.get("lang")
        echo = find_user.get("echo")
        auto_tr = find_user.get("auto_tr")

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
            await Message.send_img(chat.id, image, msg, btn)
        else:
            await Message.send_msg(chat.id, msg, btn)

    elif chat.type in ["group", "supergroup"]:
        await func_del_command(update, context)

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
        
        db = await all_db_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return
        
        find_group = db[1]
        
        title = find_group.get("title")
        lang = find_group.get("lang")
        echo = find_group.get("echo")
        auto_tr = find_group.get("auto_tr")
        welcome_msg = find_group.get("welcome_msg")
        goodbye_msg = find_group.get("goodbye_msg")
        antibot = find_group.get("antibot")
        ai_status = find_group.get("ai_status")
        del_cmd = find_group.get("del_cmd")
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        log_channel = find_group.get("log_channel")
        
        if allowed_links:
            storage, counter = "", 0
            for i in allowed_links:
                counter += 1
                if counter == len(allowed_links):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            allowed_links = storage

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
            f"• AI status: <code>{ai_status}</code>\n"
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

        btn_name_row5 = ["Links", "AI"]
        btn_data_row5 = ["links_behave", "ai_status"]

        btn_name_row6 = ["Close"]
        btn_data_row6 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
        row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

        btn = row1 + row2 + row3 + row4 + row5 + row6

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
            await Message.send_img(chat.id, image, msg, btn)
        else:
            await Message.send_msg(chat.id, msg, btn)
