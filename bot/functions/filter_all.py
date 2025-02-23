from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.translator import translate
from bot.modules.group_management.check_permission import _check_permission
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64


async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    normal_message = update.message.text or update.message.caption if update.message else None
    msg = update.message.text_html or update.message.caption_html if update.message else None

    if not msg or user.id == 777000: # Telegram channel
        return
    
    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if data_center and data_center.get("is_editing"):
        try:
            msg = int(msg)
        except ValueError:
            pass

        await LOCAL_DATABASE.insert_data("data_center", chat.id, {
            "edit_data_value": msg,
            "edit_data_value_msg_pointer_id": e_msg.id,
            "is_editing": False
        })
        return

    if chat.type == "private":
        db = await global_search("users", "user_id", user.id)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_user = db[1]
        
        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        if echo_status:
            await Message.reply_message(update, msg)

        if auto_tr_status:
            lang_code = find_user.get("lang")
            tr_msg = await translate(normal_message, lang_code)
            if tr_msg and tr_msg != normal_message:
                await Message.reply_message(update, tr_msg)
            elif not lang_code or tr_msg == False:
                btn = await Button.ubutton({"Language code's": "https://telegra.ph/Language-Code-12-24"})
                await Message.reply_message(update, "Chat language not found/invalid! Use /settings to set chat language.", btn=btn)     


    elif chat.type in ["group", "supergroup"]:
        _chk_per = await _check_permission(update, user=user)
        if not _chk_per:
            return

        if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
            await Message.send_message(chat.id, "I'm not an admin in this chat!")
            return
        
        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_group = db[1]
        
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
            if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                links_list = await RE_LINK.detect_link(msg)
                if links_list:
                    clean_msg = msg
                    allowed_links_count = 0
                    for link in links_list:
                        domain = await RE_LINK.get_domain(link)
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
                            await Message.delete_message(chat.id, e_msg)
                            await Message.send_message(chat.id, clean_msg)
                            msg_contains_link = True
                        except Exception as e:
                            logger.error(e)
        
        if echo_status and not msg_contains_link:
            await Message.reply_message(update, msg)
        
        if auto_tr_status:
            to_translate = clean_msg if msg_contains_link else normal_message
            tr_msg = await translate(to_translate, lang_code)
            if tr_msg and tr_msg != to_translate:
                await Message.reply_message(update, tr_msg)
            elif not lang_code or tr_msg == False:
                btn = await Button.ubutton({"Language code's": "https://telegra.ph/Language-Code-12-24"})
                await Message.reply_message(update, "Chat language not found/invalid! Use /settings to set chat language.", btn=btn)
        
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
                    await Message.reply_message(update, filtered_msg)
