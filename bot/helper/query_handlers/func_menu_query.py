from telegram import Update
from bot.helper.telegram_helper import Message, Button


class QueryMenus:
    async def _query_bot_settings_menu(update: Update, query):
        msg = "<u><b>Bot Settings</b></u>"

        btn_name_row1 = ["Bot pic", "Welcome img"]
        btn_data_row1 = ["query_bot_pic", "query_welcome_img"]

        btn_name_row2 = ["Images", "Support chat"]
        btn_data_row2 = ["query_images", "query_support_chat"]

        btn_name_row3 = ["Server url", "Sudo"]
        btn_data_row3 = ["query_server_url", "query_sudo"]

        btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
        btn_data_row4 = ["query_shrinkme_api", "query_omdb_api", "query_weather_api"]

        btn_name_row5 = ["> Restore DB?", "Close"]
        btn_data_row5 = ["query_restore_db", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

        btn = row1 + row2 + row3 + row4 + row5
        
        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_menu(update: Update, query, user):
        msg = (
            f"Hey, {user.first_name}! Welcome to the bot help section...\n"
            f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
            f"/start - to start the bot\n"
            f"/help - to see this message"
        )

        btn_name_row1 = ["Group Management", "AI"]
        btn_data_row1 = ["query_help_group_management_p1", "query_help_ai"]

        btn_name_row2 = ["misc", "Bot owner"]
        btn_data_row2 = ["query_help_misc_functions", "query_help_owner_functions"]

        btn_name_row3 = ["» bot.info()", "Close"]
        btn_data_row3 = ["query_help_bot_info", "query_close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, query.message, btn)
    

    async def _query_chat_settings_menu(update: Update, query, chat, find_chat):
        if chat.type == "private":
            user_mention = find_chat.get("mention")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo")
            auto_tr = find_chat.get("auto_tr")

            msg = (
                "<u><b>Chat Settings</b></u>\n\n"
                f"• User: {user_mention}\n"
                f"• ID: <code>{chat.id}</code>\n\n"

                f"• Lang: <code>{lang}</code>\n"
                f"• Auto tr: <code>{auto_tr}</code>\n"
                f"• Echo: <code>{echo}</code>\n"
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["query_chat_lang", "query_chat_auto_tr"]

            btn_name_row2 = ["Echo", "Close"]
            btn_data_row2 = ["query_chat_set_echo", "query_close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2
        else:
            title = find_chat.get("title")
            lang = find_chat.get("lang")
            echo = find_chat.get("echo")
            auto_tr = find_chat.get("auto_tr")
            welcome_user = find_chat.get("welcome_user")
            farewell_user = find_chat.get("farewell_user")
            antibot = find_chat.get("antibot")
            ai_status = find_chat.get("ai_status") or True
            del_cmd = find_chat.get("del_cmd")
            all_links = find_chat.get("all_links")
            allowed_links = find_chat.get("allowed_links")
            log_channel = find_chat.get("log_channel")
            
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
                f"• AI status: <code>{ai_status}</code>\n"
            )

            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["query_chat_lang", "query_chat_auto_tr"]

            btn_name_row2 = ["Echo", "Anti bot"]
            btn_data_row2 = ["query_chat_set_echo", "query_chat_antibot"]

            btn_name_row3 = ["Welcome", "Farewell"]
            btn_data_row3 = ["query_chat_welcome_user", "query_chat_farewell_user"]

            btn_name_row4 = ["Delete CMD", "Log channel"]
            btn_data_row4 = ["query_chat_del_cmd", "query_chat_log_channel"]

            btn_name_row5 = ["Links behave", "AI status"]
            btn_data_row5 = ["query_chat_links_behave", "query_chat_ai_status"]

            btn_name_row6 = ["Close"]
            btn_data_row6 = ["query_close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
            row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
            row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

            btn = row1 + row2 + row3 + row4 + row5 + row6

        await Message.edit_msg(update, msg, query.message, btn)
