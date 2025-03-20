from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatID, ChatType
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search
from bot.modules.translator import translate
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

def database_editing(chat, effective_message):
    data_center = MemoryDB.data_center.get(chat.id)
    if data_center and data_center.get("is_editing"):
        try:
            data_value = int(effective_message.text)
        except ValueError:
            data_value = effective_message.text

        MemoryDB.insert_data("data_center", chat.id, {
            "edit_data_value": data_value,
            "edit_value_message_id": effective_message.id,
            "is_editing": False
        })
        return True
    
    else:
        return False


async def chat_custom_filters(user, chat, effective_message, filters):
    for keyword in filters:
        message = effective_message.text or effective_message.caption

        try:
            filter_msg = message.lower()
        except AttributeError:
            filter_msg = message
        
        if keyword.lower() in filter_msg:
            filtered_msg = filters.get(keyword)
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
            await effective_message.reply_text(filtered_msg)


async def filter_text_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if user.id == ChatID.SERVICE_CHAT:
        return
    
    is_editing = database_editing(chat, effective_message)
    if is_editing != False:
        return
    
    if chat.type == ChatType.PRIVATE:
        response, database_data = database_search("users", "user_id", user.id)
        if response == False:
            await effective_message.reply_text(database_data)
            return
        
        echo_status = database_data.get("echo")
        auto_tr_status = database_data.get("auto_tr")

        if echo_status:
            await effective_message.reply_text(effective_message.text_html or effective_message.caption_html)

        if auto_tr_status:
            lang_code = database_data.get("lang")
            if lang_code:
                original_text = effective_message.text or effective_message.caption
                translated_text = translate(original_text, lang_code)

                if translated_text and translated_text.lower() != original_text.lower():
                    await effective_message.reply_text(translated_text)
                
                elif translated_text == False:
                    btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
                    await effective_message.reply_text("Invalid language code was given! Use /settings to set chat language.", reply_markup=btn)
            else:
                btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
                await effective_message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)

    elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        response, database_data = database_search("groups", "chat_id", chat.id)
        if response == False:
            await effective_message.reply_text(database_data)
            return
        
        is_links_allowed = database_data.get("is_links_allowed") # 3 values: delete; convert; None;
        allowed_links_list = database_data.get("allowed_links_list", [])
        allowed_links_list = [link.strip() for link in allowed_links_list]

        echo_status = database_data.get("echo", False)
        auto_tr_status = database_data.get("auto_tr", False)
        lang_code = database_data.get("lang")
        filters = database_data.get("filters")
        is_text_contain_links = False

        if is_links_allowed:
            chat_admins = await fetch_chat_admins(chat, user_id=user.id)
            
            if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
                links_list = RE_LINK.detect_link(effective_message.text or effective_message.caption)
                if links_list:
                    filtered_text = effective_message.text or effective_message.caption # keeping as variable to replace links later
                    allowed_links_count = 0
                    for link in links_list:
                        domain = RE_LINK.get_domain(link)
                        if domain in allowed_links_list:
                            allowed_links_count += 1
                        else:
                            if is_links_allowed == "delete":
                                filtered_text = filtered_text.replace(link, f"<code>forbidden link</code>")
                            if is_links_allowed == "convert":
                                b64_link = BASE64.encode(link)
                                filtered_text = filtered_text.replace(link, f"<code>{b64_link}</code>")
                    if allowed_links_count != len(links_list):
                        filtered_text = f"{user.mention_html()}\n\n{filtered_text}\n\n<i>Delete reason: your message contains forbidden link/s!</i>"
                        await effective_message.delete()
                        await effective_message.reply_text(filtered_text)
                        is_text_contain_links = True

        if echo_status and not is_text_contain_links:
            await effective_message.reply_text(effective_message.text_html or effective_message.caption_html)
        
        if auto_tr_status:
            if lang_code:
                to_translate = filtered_text if is_text_contain_links else (effective_message.text or effective_message.caption)
                translated_text = translate(to_translate, lang_code)
                if translated_text and translated_text.lower() != to_translate.lower():
                    text = (
                        f"{translated_text}\n\n"
                        f"• <a href='{effective_message.link}'>{effective_message.id}</a> | {user.mention_html()}"
                    )
                    await effective_message.reply_text(text)
                elif translated_text == False:
                    btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
                    await effective_message.reply_text("Invalid language code was given! Use /settings to set chat language.", reply_markup=btn)
            else:
                btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
                await effective_message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)

        if filters:
            await chat_custom_filters(user, chat, effective_message, filters) 
