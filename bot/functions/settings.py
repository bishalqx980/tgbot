import random
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.combined_db import find_bot_docs
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    _bot = await find_bot_docs()
    if not _bot:
        return

    if chat.type == "private":
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "collection_name": "users",
            "db_find": "user_id",
            "db_vlaue": user.id,
            "edit_data_key": None,
            "edit_data_value": None,
            "del_msg_pointer_id": e_msg.id,
            "edit_data_value_msg_pointer_id": None
        }

        await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

        db = await global_search("users", "user_id", user.id)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_user = db[1]
        
        user_mention = find_user.get("mention")
        lang = find_user.get("lang")
        echo = find_user.get("echo", False)
        auto_tr = find_user.get("auto_tr", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• User: {user_mention}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n\n"
        )

        btn_data = [
            {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
            {"Echo": "query_chat_set_echo", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        _bot = await find_bot_docs()
        
        images = _bot.get("images")
        if images:
            image = random.choice(images).strip()
        else:
            image = _bot.get("bot_pic")

        if image:
            await Message.reply_image(update, image, msg, btn=btn)
        else:
            await Message.reply_message(update, msg, btn=btn)

    elif chat.type in ["group", "supergroup"]:
        await func_del_command(update, context)

        if user.is_bot:
            await Message.reply_message(update, "I don't take permission from anonymous admins!")
            return
        
        sent_msg = await Message.reply_message(update, "💭")
        _chk_per = await _check_permission(update, user=user)
        if not _chk_per:
            await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
            return
            
        if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
            await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
            return
        
        if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            await Message.edit_message(update, "You aren't an admin in this chat!", sent_msg)
            return
        
        if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
            if not _chk_per["user_permission"].can_change_info:
                await Message.edit_message(update, "You don't have enough rights to manage this chat!", sent_msg)
                return
        
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "collection_name": "groups",
            "db_find": "chat_id",
            "db_vlaue": chat.id,
            "edit_data_key": None,
            "edit_data_value": None,
            "del_msg_pointer_id": e_msg.id,
            "edit_data_value_msg_pointer_id": None
        }
        
        await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.edit_message(update, db[1], sent_msg)
            return
        
        find_group = db[1]
        
        title = find_group.get("title")
        lang = find_group.get("lang")
        echo = find_group.get("echo", False)
        auto_tr = find_group.get("auto_tr", False)
        welcome_user = find_group.get("welcome_user", False)
        farewell_user = find_group.get("farewell_user", False)
        antibot = find_group.get("antibot", False)
        del_cmd = find_group.get("del_cmd", False)
        all_links = find_group.get("all_links", False)
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
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
            f"• Welcome user: <code>{welcome_user}</code>\n"
            f"• Farewell user: <code>{farewell_user}</code>\n"
            f"• Delete CMD: <code>{del_cmd}</code>\n"
            f"• Log channel: <code>{log_channel}</code>\n"
            f"• All links: <code>{all_links}</code>\n"
            f"• Allowed links: <code>{allowed_links}</code>\n"
        )

        btn_data = [
            {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
            {"Echo": "query_chat_set_echo", "Anti bot": "query_chat_antibot"},
            {"Welcome": "query_chat_welcome_user", "Farewell": "query_chat_farewell_user"},
            {"Delete CMD": "query_chat_del_cmd", "Log channel": "query_chat_log_channel"},
            {"Links behave": "query_chat_links_behave", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        _bot = await find_bot_docs()
        
        images = _bot.get("images")
        if images:
            image = random.choice(images).strip()
        else:
            image = _bot.get("bot_pic")
        
        if image:
            await Message.reply_image(update, image, msg, btn=btn)
            await Message.delete_message(chat.id, sent_msg)
        else:
            await Message.edit_message(update, msg, sent_msg, btn)
