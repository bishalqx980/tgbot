from telegram import Update
from bot.helper.telegram_helper import Message, Button
from bot.helper.query_handlers.query_functions import QueryFunctions
from bot.modules.database.local_database import LOCAL_DATABASE


class QueryChatSettings:
    async def _query_chat_lang(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "lang"})
        lang = find_chat.get("lang")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Language code: <code>{lang}</code>\n\n"
            "<i><b>Note</b>: Get your country language code from the below link!\neg. English language code is <code>en</code></i>"
        )

        btn_name_row1 = ["Language code's"]
        btn_url_row1 = ["https://telegra.ph/Language-Code-12-24"]

        btn_name_row2 = ["Edit Value"]
        btn_data_row2 = ["query_edit_value"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_auto_tr(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "auto_tr"})
        auto_tr = find_chat.get("auto_tr")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Auto translate: <code>{auto_tr}</code>\n\n"
            "<i><b>Note</b>: This will automatically translate chat conversation into chat default language!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_set_echo(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "echo"})
        echo = find_chat.get("echo")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Echo: <code>{echo}</code>\n\n"
            "<i><b>Note</b>: This will repeat user message!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_welcome_msg(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "welcome_msg"})
        welcome_msg = find_chat.get("welcome_msg")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Welcome user: <code>{welcome_msg}</code>\n\n"
            "<i><b>Note</b>: This will welcome the new chat member!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Set custom message"]
        btn_data_row2 = ["query_set_custom_welcome_msg"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_set_custom_welcome_msg(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "custom_welcome_msg"})
        custom_welcome_msg = find_chat.get("custom_welcome_msg")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Welcome message\n--------------------\n<code>{custom_welcome_msg}</code>\n\n"
            "<i><b>Note</b>: This message will be send as greeting message in the chat when a user join! (supports telegram formatting)</i>"
        )

        btn_name_row1 = ["Set default message", "Set custom message"]
        btn_data_row1 = ["query_rm_value", "query_edit_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_welcome_msg", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_farewell_msg(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "farewell_msg"})
        farewell_msg = find_chat.get("farewell_msg")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Farewell message: <code>{farewell_msg}</code>\n\n"
            "<i><b>Note</b>: This will send a farewell message to chat when a user left!\n</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_antibot(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "antibot"})
        antibot = find_chat.get("antibot")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Antibot: <code>{antibot}</code>\n\n"
            "<i><b>Note</b>: This will prevent other bot from joining in chat!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_chat_del_cmd(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "del_cmd"})
        del_cmd = find_chat.get("del_cmd")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Delete cmd: <code>{del_cmd}</code>\n\n"
            "<i><b>Note</b>: This will delete bot commands when you will send a command in chat!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_chat_log_channel(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "log_channel"})
        log_channel = find_chat.get("log_channel")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"Log channel: <code>{log_channel}</code>\n\n"
            "<i><b>Note</b>: This will log every actions occurred in your chat (ban, kick, mute, etc.) using bot!\nAdd the bot in a channel as admin where you want to log, then you will get a message with chat_id from bot, pass the chat_id using edit value!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["query_edit_value", "query_rm_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_chat_links_behave(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        all_links = find_chat.get("all_links")
        allowed_links = find_chat.get("allowed_links")

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
            f"All links: <code>{all_links}</code>\n"
            f"Allowed links: <code>{allowed_links}</code>\n\n"
            "<i><b>Note</b>: Select whether it will delete or convert the links into base64 or do nothing if links in message!</i>\n\n"
            "<i>Allowed links » these links won't be deleted!</i>\n"
            "<i>Delete links » replace the links with `forbidden link`</i>\n\n"
            "<i>Echo/Auto translate won't work if message contains link!</i>"
        )

        btn_name_row1 = ["All links", "Allowed links"]
        btn_data_row1 = ["query_chat_all_links", "query_chat_allowed_links"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_chat_all_links(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        all_links = find_chat.get("all_links")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"All links: <code>{all_links}</code>\n\n"
            "<i><b>Note</b>: Select whether bot will delete the message or convert link into base64 or do nothing!</i>"
        )

        btn_name_row1 = ["Delete", "Convert", "Nothing"]
        btn_data_row1 = ["query_d_links", "query_c_links", "query_none_links"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_links_behave", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_chat_allowed_links(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "allowed_links"})
        allowed_links = find_chat.get("allowed_links")
        
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
            f"Allowed links: <code>{allowed_links}</code>\n\n"
            "<i><b>Note</b>: Send domain name of allowed links eg. <code>google.com</code> multiple domain will be separated by comma!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["query_edit_value", "query_rm_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_links_behave", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_d_links(query, chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        await QueryFunctions.query_edit_value(chat.id, query, "delete")


    async def _query_c_links(query, chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        await QueryFunctions.query_edit_value(chat.id, query, "convert")
    

    async def _query_none_links(query, chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "links_behave"})
        await QueryFunctions.query_edit_value(chat.id, query, None)
    

    async def _query_chat_ai_status(update: Update, query, chat, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": "ai_status"})
        ai_status = find_chat.get("ai_status")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"AI status: <code>{ai_status}</code>\n\n"
            "<i><b>Note</b>: Enable / Disbale AI functions in chat!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["query_true", "query_false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["query_chat_settings_menu", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, query.message, btn)
