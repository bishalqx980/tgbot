from telegram import Update
from telegram.constants import ChatType
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.messages_storage import (
    help_menu,
    bot_settings_menu,
    chat_settings_menu_pvt,
    chat_settings_menu_group
)
from bot.modules.database import MemoryDB

class QueryMenus:
    async def _query_chat_settings_menu(update: Update, find_chat):
        chat = update.effective_chat
        effective_message = update.effective_message

        if chat.type == ChatType.PRIVATE:
            user_mention = find_chat.get("mention")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo", False)
            auto_tr = find_chat.get("auto_tr", False)

            text = chat_settings_menu_pvt.format(
                user_mention,
                chat.id,
                lang,
                auto_tr,
                echo
            )

            btn_data = [
                {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
                {"Echo": "query_chat_set_echo", "Close": "query_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)
        
        else:
            title = find_chat.get("title")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo", False)
            auto_tr = find_chat.get("auto_tr", False)
            welcome_user = find_chat.get("welcome_user", False)
            farewell_user = find_chat.get("farewell_user", False)
            antibot = find_chat.get("antibot", False)
            is_links_allowed = find_chat.get("is_links_allowed")
            allowed_links_list = find_chat.get("allowed_links_list")
            
            if allowed_links_list:
                allowed_links_list = ", ".join(allowed_links_list)

            text = chat_settings_menu_group.format(
                title,
                chat.id,
                lang,
                auto_tr,
                echo,
                antibot,
                welcome_user,
                farewell_user,
                is_links_allowed,
                allowed_links_list
            )

            btn_data = [
                {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
                {"Echo": "query_chat_set_echo", "Anti bot": "query_chat_antibot"},
                {"Welcome": "query_chat_welcome_user", "Farewell": "query_chat_farewell_user"},
                {"Links": "query_chat_links_behave", "Close": "query_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)
        
        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)
