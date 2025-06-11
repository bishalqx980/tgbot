from telegram import Update
from telegram.ext import ContextTypes
from bot import TL_LANG_CODES_URL
from bot.helpers import BuildKeyboard
from bot.utils.database.common import database_search
from bot.modules.translator import translate
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64
from ..group_management.auxiliary.chat_admins import ChatAdmins
from .edit_database import edit_database

async def filter_public_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    is_editing = edit_database(chat.id, user.id, effective_message)
    if is_editing:
        return

    chat_data = database_search("chats_data", "chat_id", chat.id)
    if not chat_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    links_behave = chat_data.get("links_behave") # 3 values: delete; convert; None;
    allowed_links = chat_data.get("allowed_links") or []
    allowed_links = [link.strip() for link in allowed_links]

    echo_status = chat_data.get("echo")
    auto_tr_status = chat_data.get("auto_tr")
    lang_code = chat_data.get("lang")
    filters = chat_data.get("filters")
    is_text_contain_links = False

    if links_behave:
        chat_admins = ChatAdmins()
        await chat_admins.fetch_admins(chat, user_id=user.id)
        
        if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
            links_list = RE_LINK.detect_link(effective_message.text or effective_message.caption)
            if links_list:
                filtered_text = effective_message.text or effective_message.caption # keeping as variable to replace links later
                allowed_links_count = 0
                for link in links_list:
                    domain = RE_LINK.get_domain(link)
                    if domain in allowed_links:
                        allowed_links_count += 1
                    else:
                        if links_behave == "delete":
                            filtered_text = filtered_text.replace(link, f"<code>forbidden link</code>")
                        if links_behave == "convert":
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
                try:
                    await effective_message.reply_text(f"{user.mention_html()}: {translated_text}")
                except:
                    pass
            
            elif translated_text == False:
                btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
                await effective_message.reply_text("Invalid language code was given! Use /settings to set chat language.", reply_markup=btn)
        else:
            btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
            await effective_message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)

    if filters:
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
