from telegram import Update
from bot.helper.telegram_helper import Message, Button
from bot.helper.query_handlers.query_functions import QueryFunctions
from bot.modules.database.local_database import LOCAL_DATABASE


class QueryChatSettings:
    async def _query_chat_lang(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "lang"})
        lang = find_chat.get("lang")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Language code: <code>{lang}</code>\n\n"
            "<i><b>Note:</b> Get your country language code from the link below!\nE.g. English language code is <code>en</code></i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn1 = await Button.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
        btn2 = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn1 + btn2)


    async def _query_chat_auto_tr(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "auto_tr"})
        auto_tr = find_chat.get("auto_tr", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Auto translate: <code>{auto_tr}</code>\n\n"
            "<i><b>Note:</b> This will automatically translate chat conversation into chat default language!</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_chat_set_echo(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "echo"})
        echo = find_chat.get("echo", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Echo: <code>{echo}</code>\n\n"
            "<i><b>Note:</b> This will repeat user message!</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_chat_welcome_user(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "welcome_user"})
        welcome_user = find_chat.get("welcome_user", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Welcome user: <code>{welcome_user}</code>\n\n"
            "<i><b>Note:</b> This will welcome the new chat member!</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Custom welcome message": "query_set_custom_welcome_msg"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_set_custom_welcome_msg(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "custom_welcome_msg"})
        custom_welcome_msg = find_chat.get("custom_welcome_msg") or "default message"
        is_sent_below = None
        if len(custom_welcome_msg) > 100:
            custom_welcome_msg = "Sent below..."
            is_sent_below = True

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Welcome message:\n<code>{custom_welcome_msg}</code>\n\n"
            "<i><b>Note:</b> This message will be send as greeting message in the chat when a user join! (supports telegram formatting)</i>\n\n"
            "<b><u>Text formatting</u></b>\n"
            "<code>{first}</code> first name\n"
            "<code>{last}</code> last name\n"
            "<code>{fullname}</code> fullname\n"
            "<code>{username}</code> username\n"
            "<code>{mention}</code> mention\n"
            "<code>{id}</code> id\n"
            "<code>{chatname}</code> chat title\n"
        )

        btn_data = [
            {"Set default message": "query_rm_value"},
            {"Set custom message": "query_edit_value"},
            {"Back": "query_chat_welcome_user", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
        if is_sent_below:
            await Message.reply_message(update, find_chat.get("custom_welcome_msg"))


    async def _query_chat_farewell_user(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "farewell_user"})
        farewell_user = find_chat.get("farewell_user", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Farewell user: <code>{farewell_user}</code>\n\n"
            "<i><b>Note:</b> This will send a farewell message to chat when a user left!\n</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_chat_antibot(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "antibot"})
        antibot = find_chat.get("antibot", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Antibot: <code>{antibot}</code>\n\n"
            "<i><b>Note:</b> This will prevent other bot from joining in chat!</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_chat_del_cmd(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "del_cmd"})
        del_cmd = find_chat.get("del_cmd", False)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Delete CMD: <code>{del_cmd}</code>\n\n"
            "<i><b>Note:</b> This will delete bot commands when you will send a command in chat!</i>"
        )

        btn_data = [
            {"Enable": "query_true", "Disable": "query_false"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_chat_log_channel(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "log_channel"})
        log_channel = find_chat.get("log_channel")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Log channel: <code>{log_channel}</code>\n\n"
            "<i><b>Note:</b> This will log every actions occurred in your chat (ban, kick, mute, etc.) using bot!\nAdd the bot in a channel as admin where you want to log, then you will get a message with chat_id from bot, pass the chat_id using edit value!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_chat_links_behave(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        all_links = find_chat.get("all_links")
        allowed_links = find_chat.get("allowed_links")
        if allowed_links:
            allowed_links = ", ".join(allowed_links)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"All links: <code>{all_links}</code>\n"
            f"Allowed links: <code>{allowed_links}</code>\n\n"
            "<i><b>Note:</b> Select whether it will delete or convert the links into base64 or do nothing if links in message!</i>\n\n"
            "<i>Allowed links » these links won't be deleted!</i>\n"
            "<i>Delete links » replace the links with `forbidden link`</i>\n\n"
            "<i>Echo/Auto translate won't work if message contains link!</i>"
        )

        btn_data = [
            {"All links": "query_chat_all_links", "Allowed links": "query_chat_allowed_links"},
            {"Back": "query_chat_settings_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_chat_all_links(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        all_links = find_chat.get("all_links")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"All links: <code>{all_links}</code>\n\n"
            "<i><b>Note:</b> Select whether bot will delete the message or convert link into base64 or do nothing!</i>"
        )

        btn_data = [
            {"Delete": "query_d_links", "Convert": "query_c_links", "Nothing": "query_none_links"},
            {"Back": "query_chat_links_behave", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_chat_allowed_links(update: Update, query, find_chat):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "allowed_links"})
        allowed_links = find_chat.get("allowed_links")
        if allowed_links:
            allowed_links = ", ".join(allowed_links)

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Allowed links: <code>{allowed_links}</code>\n\n"
            "<i><b>Note:</b> Send domain name of allowed links eg. <code>google.com</code> multiple domain will be separated by comma!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_chat_links_behave", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_d_links(update: Update, query):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "all_links"})
        await QueryFunctions.query_edit_value(chat.id, query, "delete")


    async def _query_c_links(update: Update, query):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "all_links"})
        await QueryFunctions.query_edit_value(chat.id, query, "convert")
    

    async def _query_none_links(update: Update, query):
        chat = update.effective_chat
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "all_links"})
        await QueryFunctions.query_edit_value(chat.id, query, None)
