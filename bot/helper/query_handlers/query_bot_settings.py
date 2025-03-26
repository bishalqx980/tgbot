from telegram import Update
from bot.update_db import update_database
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

class QueryBotSettings:
    async def _query_bot_pic(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "bot_pic"})
        bot_pic = database_data.get("bot_pic")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Bot pic (link): <code>{bot_pic}</code>\n\n"
            "<i><b>Note:</b> Send an image url/link to set bot pic!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_images(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "images"})
        images = database_data.get("images")
        if images:
            images = ", ".join(images)
        
        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Images (link): <code>{images}</code>\n\n"
            "<i><b>Note:</b> Single image or send multiple image link separated by comma!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]
        
        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            is_sent = await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            is_sent = await effective_message.edit_caption(text, reply_markup=btn)

        if not is_sent:
            with open("temp/temp.txt", "w") as f:
                f.write(images)
            
            with open("temp/temp.txt", "rb") as f:
                tmp_file = f.read()
            
            await effective_message.reply_document(tmp_file, "image links", filename="image links.txt")
            
            text = (
                "<u><b>Bot Settings</b></u>\n\n"
                f"Images (link): <code>Text file sent below!</code>\n\n"
                "<i><b>Note:</b> Single image or send multiple image link separated by comma!</i>"
            )

            if effective_message.text:
                await effective_message.edit_text(text, reply_markup=btn)
            elif effective_message.caption:
                await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_support_chat(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "support_chat"})
        support_chat = database_data.get("support_chat")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Support Chat (link): <code>{support_chat}</code>\n"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_server_url(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "server_url"})
        server_url = database_data.get("server_url")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Server url: <code>{server_url}</code>\n\n"
            "<i><b>Note:</b> Bot will fall asleep if you deployed the bot on render (free) and don't set this value. (Bot restart required)</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_sudo(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "sudo_users"})
        sudo_users = database_data.get("sudo_users")
        if sudo_users:
            sudo_users = ", ".join(str(i) for i in sudo_users)
        
        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Sudo users: <code>{sudo_users}</code>\n\n"
            "<i><b>Note:</b> The power user! Sudo users have owner function access!\nAdd user_id eg. <code>2134776547</code>\nmultiple id will be separated by comma!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_shrinkme_api(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "shrinkme_api"})
        shrinkme_api = database_data.get("shrinkme_api")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Shrinkme API: <code>{shrinkme_api}</code>\n\n"
            "<i><b>Note:</b> This api for /shorturl command!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_omdb_api(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "omdb_api"})
        omdb_api = database_data.get("omdb_api")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"OMDB API: <code>{omdb_api}</code>\n\n"
            "<i><b>Note:</b> This api for /movie command!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_weather_api(update: Update, database_data):
        user = update.effective_user
        effective_message = update.effective_message

        MemoryDB.insert_data("data_center", user.id, {"edit_data_key": "weather_api"})
        weather_api = database_data.get("weather_api")

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            f"Weather API: <code>{weather_api}</code>\n\n"
            "<i><b>Note:</b> This api for /weather command!</i>"
        )

        btn_data = [
            {"Edit Value": "query_edit_value"},
            {"Remove Value": "query_rm_value"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_restore_db(update: Update):
        effective_message = update.effective_message

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "<b>» ⚠ Restore Database</b>\n"
            "- <i>This will clear all bot data (excluding user & group data) from online database and restore data from the <code>config.env</code> file.</i>\n\n"
            "<b>» 💾 Clear Memory Cache</b>\n"
            "- <i>This will clear local database cache.</i>\n\n"
            "<i><b>Note:</b> Use <code>⚠ Restore Database</code> with caution!</i>"
        )

        btn_data = [
            {"⚠ Restore Database": "query_confirm_restore_db"},
            {"💾 Clear Memory Cache": "query_clear_memory_cache"},
            {"Back": "query_bot_settings_menu", "Close": "query_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)

        if effective_message.text:
            await effective_message.edit_text(text, reply_markup=btn)
        elif effective_message.caption:
            await effective_message.edit_caption(text, reply_markup=btn)


    async def _query_confirm_restore_db(update: Update):
        effective_message = update.effective_message
        res = MongoDB.delete_all_doc("bot_data")
        update_database()
        text = "Database has been restored successfully from <code>config.env</code>!" if res else "Something went wrong! Check /log"
        await effective_message.reply_text(text)


    async def _query_clear_memory_cache(update: Update):
        effective_message = update.effective_message
        MemoryDB.clear_all()
        update_database()
        await effective_message.reply_text("Local database has been cleared!")
