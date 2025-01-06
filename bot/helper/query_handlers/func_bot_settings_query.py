from telegram import Update
from bot.update_db import update_database
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


class QueryBotSettings:
    async def _query_bot_pic(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "bot_pic"})
        bot_pic = find_chat.get("bot_pic")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Bot pic (link): <code>{bot_pic}</code>\n\n"
            "<i><b>Note:</b> Send an image url/link to set bot pic!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_welcome_img(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "welcome_img"})
        welcome_img = find_chat.get("welcome_img")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Welcome img: {welcome_img}\n\n"
            "<i><b>Note:</b> Should bot show image on start?</i>"
        )

        btn_data_row1 = {
            "Yes": "query_true",
            "No": "query_false"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1, True)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_images(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "images"})
        images = find_chat.get("images")

        if images:
            storage, counter = "", 0
            for i in images:
                counter += 1
                if counter == len(images):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            images = storage
        
        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Images (link): <code>{images}</code>\n\n"
            "<i><b>Note:</b> Single image or send multiple image link separated by comma!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        sent_msg = await Message.edit_message(update, msg, query.message, btn)

        if not sent_msg:
            open("tmp.txt", "w").write(images)
            tmp_file = open("tmp.txt", "rb").read()
            await Message.send_document(user.id, tmp_file, "image links.txt", "image links")
            
            msg = (
                "<u><b>Bot Settings</b></u>\n\n"
                f"Images (link): <code>Text file sent below!</code>\n\n"
                "<i><b>Note:</b> Single image or send multiple image link separated by comma!</i>"
            )

            await Message.edit_message(update, msg, query.message, btn)


    async def _query_support_chat(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "support_chat"})
        support_chat = find_chat.get("support_chat")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Support Chat (link): <code>{support_chat}</code>\n"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_server_url(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "server_url"})
        server_url = find_chat.get("server_url")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Server url: <code>{server_url}</code>\n\n"
            "<i><b>Note:</b> Bot will fall asleep if you deployed the bot on render (free) and don't set this value...</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_sudo(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "sudo_users"})
        sudo_users = find_chat.get("sudo_users")

        if sudo_users:
            storage, counter = "", 0
            for i in sudo_users:
                counter += 1
                if counter == len(sudo_users):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            sudo_users = storage

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Sudo users: <code>{sudo_users}</code>\n\n"
            "<i><b>Note:</b> The power user! Sudo users have owner function access!\nAdd user_id eg. <code>2134776547</code></i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_shrinkme_api(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "shrinkme_api"})
        shrinkme_api = find_chat.get("shrinkme_api")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Shrinkme API: <code>{shrinkme_api}</code>\n\n"
            "<i><b>Note:</b> This api for /short command!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_omdb_api(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "omdb_api"})
        omdb_api = find_chat.get("omdb_api")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"OMDB API: <code>{omdb_api}</code>\n\n"
            "<i><b>Note:</b> This api for /movie command!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_weather_api(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "weather_api"})
        weather_api = find_chat.get("weather_api")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Weather API: <code>{weather_api}</code>\n\n"
            "<i><b>Note:</b> This api for /weather command!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_imgbb_api(update: Update, query, user, find_chat):
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"edit_data_key": "imgbb_api"})
        imgbb_api = find_chat.get("imgbb_api")

        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"ImgBB API: <code>{imgbb_api}</code>\n\n"
            "<i><b>Note:</b> This api for /itl command!</i>"
        )

        btn_data_row1 = {
            "Edit Value": "query_edit_value",
            "Remove Value": "query_rm_value"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_restore_db(update: Update, query):
        msg = (
            "<u><b>Bot Settings</b></u>\n\n"
            "<b>» ⚠ Restore Database</b>\n"
            "- <i>This will clear all bot data (excluding user & group data) from online database and restore data from the <code>config.env</code> file.</i>\n\n"
            "<b>» ♻️ Clear LocalDB Cache</b>\n"
            "- <i>This will clear local database cache.</i>\n\n"
            "<i><b>Note:</b> Use <code>⚠ Restore Database</code> with caution!</i>"
        )

        btn_data_row1 = {
            "⚠ Restore Database": "query_confirm_restore_db",
            "♻️ Clear LocalDB Cache": "query_clear_localdb_cache"
        }

        btn_data_row2 = {
            "Back": "query_bot_settings_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_confirm_restore_db(update: Update, data_center):
        res1 = await MongoDB.delete_all_doc("bot_docs")
        res2 = await update_database()
        msg = "Database has been restored successfully from <code>config.env</code>!" if res1 and res2 else "Something went wrong! Check /log"
        await Message.send_message(data_center.get("chat_id"), msg)


    async def _query_clear_localdb_cache(update: Update, data_center):
        res = await LOCAL_DATABASE.restore_db()
        await update_database()
        msg = "LocalDB cache has been cleared!" if res else "Something went wrong! Check /log"
        await Message.send_message(data_center.get("chat_id"), msg)
