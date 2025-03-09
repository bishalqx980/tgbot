from telegram import Update
from telegram.constants import ChatType
from bot.helper.telegram_helpers.telegram_helper import Message, Button

class QueryMenus:
    async def _query_bot_settings_menu(update: Update, query):
        msg = "<u><b>Bot Settings</b></u>"
        btn_data = [
            {"Bot pic": "query_bot_pic", "Images": "query_images"},
            {"Support chat": "query_support_chat", "Server url": "query_server_url"},
            {"Sudo": "query_sudo", "Shrinkme API": "query_shrinkme_api"},
            {"OMDB API": "query_omdb_api", "Weather API": "query_weather_api"},
            {"> Restore DB?": "query_restore_db", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_menu(update: Update, query):
        user = update.effective_user
        msg = (
            f"Hey, {user.full_name}! Welcome to the bot help section.\n"
            "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
            "/start - to start the bot\n"
            "/help - to see this message\n\n"
            "<b>Note:</b> <i>The bot is compatible with the <code>/</code>, <code>!</code>, <code>.</code> and <code>-</code> command prefixes.</i>"
        )

        btn_data = [
            {"Group Management": "query_help_group_management_p1", "AI": "query_help_ai"},
            {"misc": "query_help_misc_functions", "Bot owner": "query_help_owner_functions"},
            {"» bot.info()": "query_help_bot_info", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_chat_settings_menu(update: Update, query, find_chat):
        chat = update.effective_chat

        if chat.type == ChatType.PRIVATE:
            user_mention = find_chat.get("mention")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo", False)
            auto_tr = find_chat.get("auto_tr", False)

            msg = (
                "<u><b>Chat Settings</b></u>\n\n"
                f"• User: {user_mention}\n"
                f"• ID: <code>{chat.id}</code>\n\n"

                f"• Lang: <code>{lang}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
            )

            btn_data = [
                {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
                {"Echo": "query_chat_set_echo", "Close": "query_close"}
            ]

            btn = await Button.cbutton(btn_data)
        
        else:
            title = find_chat.get("title")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo", False)
            auto_tr = find_chat.get("auto_tr", False)
            welcome_user = find_chat.get("welcome_user", False)
            farewell_user = find_chat.get("farewell_user", False)
            antibot = find_chat.get("antibot", False)
            del_cmd = find_chat.get("del_cmd", False)
            all_links = find_chat.get("all_links")
            allowed_links = find_chat.get("allowed_links")
            log_channel = find_chat.get("log_channel")
            
            if allowed_links:
                allowed_links = ", ".join(allowed_links)

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

        await Message.edit_message(update, msg, query.message, btn)
