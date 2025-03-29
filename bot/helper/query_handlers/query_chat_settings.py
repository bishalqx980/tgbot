from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.query_handlers.query_functions import QueryFunctions
from bot.modules.database import MemoryDB

class QueryChatSettings:
    async def _query_chat_links_behave(update: Update, find_chat):
        effective_message = update.effective_message

        is_links_allowed = find_chat.get("is_links_allowed")
        allowed_links_list = find_chat.get("allowed_links_list")
        if allowed_links_list:
            allowed_links_list = ", ".join(allowed_links_list)

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            f"All links: <code>{is_links_allowed}</code>\n"
            f"Allowed links: <code>{allowed_links_list}</code>\n\n"
            "<blockquote><b>Note:</b> Select whether it will delete or convert the links into base64 or do nothing if links in message!</blockquote>\n\n"
            "<i>Allowed links » these links won't be deleted!</i>\n"
            "<i>Delete links » replace the links with `forbidden link`</i>\n\n"
            "<i>Echo/Auto translate won't work if message contains link!</i>"
        )

        btn_data = [
            {"All links": "query_chat_is_links_allowed", "Allowed links": "query_chat_allowed_links_list"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_chat_is_links_allowed(update: Update, find_chat):
        effective_message = update.effective_message
        
        is_links_allowed = find_chat.get("is_links_allowed")

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            f"All links: <code>{is_links_allowed}</code>\n\n"
            "<blockquote><b>Note:</b> Select whether bot will delete the message or convert link into base64 or do nothing!</blockquote>"
        )

        btn_data = [
            {"Delete": "query_d_links", "Convert": "query_c_links", "Nothing": "query_none_links"},
            {"Back": "query_chat_links_behave", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)
    

    async def _query_chat_allowed_links_list(update: Update, find_chat):
        chat = update.effective_chat
        effective_message = update.effective_message

        MemoryDB.insert("data_center", chat.id, {"update_data_key": "allowed_links_list"})
        allowed_links_list = find_chat.get("allowed_links_list")
        if allowed_links_list:
            allowed_links_list = ", ".join(allowed_links_list)

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            f"Allowed links: <code>{allowed_links_list}</code>\n\n"
            "<blockquote><b>Note:</b> Send domain name of allowed links eg. <code>google.com</code> multiple domain will be separated by comma!</blockquote>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_chat_links_behave", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)
    

    async def _query_d_links(update: Update, context: ContextTypes.DEFAULT_TYPE, query):
        chat = update.effective_chat
        MemoryDB.insert("data_center", chat.id, {"update_data_key": "is_links_allowed"})
        await QueryFunctions.query_edit_value(context, chat.id, query, "delete")


    async def _query_c_links(update: Update, context: ContextTypes.DEFAULT_TYPE, query):
        chat = update.effective_chat
        MemoryDB.insert("data_center", chat.id, {"update_data_key": "is_links_allowed"})
        await QueryFunctions.query_edit_value(context, chat.id, query, "convert")
    

    async def _query_none_links(update: Update, context: ContextTypes.DEFAULT_TYPE, query):
        chat = update.effective_chat
        MemoryDB.insert("data_center", chat.id, {"update_data_key": "is_links_allowed"})
        await QueryFunctions.query_edit_value(context, chat.id, query, None)
