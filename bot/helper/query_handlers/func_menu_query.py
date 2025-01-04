from telegram import Update
from bot.helper.telegram_helper import Message, Button


class QueryMenus:
    async def _query_bot_settings_menu(update: Update, query):
        msg = "<u><b>Bot Settings</b></u>"

        btn_data_row1 = {
            "Bot pic": "query_bot_pic",
            "Welcome img": "query_welcome_img"
        }

        btn_data_row2 = {
            "Images": "query_images",
            "Support chat": "query_support_chat"
        }

        btn_data_row3 = {
            "Server url": "query_server_url",
            "Sudo": "query_sudo"
        }

        btn_data_row4 = {
            "Shrinkme API": "query_shrinkme_api",
            "OMDB API": "query_omdb_api"
        }

        btn_data_row5 = {
            "Weather API": "query_weather_api",
            "ImgBB API": "query_imgbb_api"
        }

        btn_data_row6 = {
            "> Restore DB?": "query_restore_db",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1, True)
        row2 = await Button.cbutton(btn_data_row2, True)
        row3 = await Button.cbutton(btn_data_row3, True)
        row4 = await Button.cbutton(btn_data_row4, True)
        row5 = await Button.cbutton(btn_data_row5, True)
        row6 = await Button.cbutton(btn_data_row6, True)

        btn = row1 + row2 + row3 + row4 + row5 + row6
        
        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_menu(update: Update, query, user):
        msg = (
            f"Hey, {user.full_name}! Welcome to the bot help section.\n"
            "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
            "/start - to start the bot\n"
            "/help - to see this message\n\n"
            "<b>Note:</b> <i>The bot is compatible with the <code>/</code>, <code>!</code>, and <code>.</code> command prefixes.</i>"
        )

        btn_data_row1 = {
            "Group Management": "query_help_group_management_p1",
            "AI": "query_help_ai"
        }

        btn_data_row2 = {
            "misc": "query_help_misc_functions",
            "Bot owner": "query_help_owner_functions"
        }

        btn_data_row3 = {
            "» bot.info()": "query_help_bot_info",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1, True)
        row2 = await Button.cbutton(btn_data_row2, True)
        row3 = await Button.cbutton(btn_data_row3, True)

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

            btn_data_row1 = {
                "Language": "query_chat_lang",
                "Auto translate": "query_chat_auto_tr"
            }

            btn_data_row2 = {
                "Echo": "query_chat_set_echo",
                "Close": "query_close"
            }

            row1 = await Button.cbutton(btn_data_row1, True)
            row2 = await Button.cbutton(btn_data_row2, True)

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

            btn_data_row1 = {
                "Language": "query_chat_lang",
                "Auto translate": "query_chat_auto_tr"
            }

            btn_data_row2 = {
                "Echo": "query_chat_set_echo",
                "Anti bot": "query_chat_antibot"
            }

            btn_data_row3 = {
                "Welcome": "query_chat_welcome_user",
                "Farewell": "query_chat_farewell_user"
            }

            btn_data_row4 = {
                "Delete CMD": "query_chat_del_cmd",
                "Log channel": "query_chat_log_channel"
            }

            btn_data_row5 = {
                "Links behave": "query_chat_links_behave",
                "AI status": "query_chat_ai_status"
            }

            btn_data_row6 = {
                "Close": "query_close"
            }

            row1 = await Button.cbutton(btn_data_row1, True)
            row2 = await Button.cbutton(btn_data_row2, True)
            row3 = await Button.cbutton(btn_data_row3, True)
            row4 = await Button.cbutton(btn_data_row4, True)
            row5 = await Button.cbutton(btn_data_row5, True)
            row6 = await Button.cbutton(btn_data_row6)

            btn = row1 + row2 + row3 + row4 + row5 + row6

        await Message.edit_msg(update, msg, query.message, btn)
