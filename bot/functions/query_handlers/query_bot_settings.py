import json
from telegram import Update
from telegram.ext import ContextTypes
from bot.update_db import update_database
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

async def query_bot_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("bsettings_")

    # memory access
    data_center = MemoryDB.data_center.get(user.id)
    if not data_center:
        await query.answer("Session Expired.")
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(user.id, [message_id, message_id - 1])
        except:
            pass
        return
    
    # memory accessed data
    text = data_center.get("text") # main menu text
    btn = data_center.get("btn") # main menu btn
    is_caption = data_center.get("is_caption")
    is_editing_btn = None

    if query_data == "menu":
        # accessing bot data
        bot_data = MemoryDB.bot_data
        # formatting the message
        text = text.format(
            bot_data.get("bot_pic"),
            len(bot_data.get("images") or []),
            bot_data.get("support_chat"),
            bot_data.get("server_url"),
            len(bot_data.get("sudo_users") or []),
            bot_data.get("shrinkme_api"),
            bot_data.get("omdb_api"),
            bot_data.get("weather_api")
        )
    
    elif query_data == "bot_pic":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "bot_pic",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Bot Photo (link): <code>{}</code>\n\n"
            "<i><b>Note:</b> Send an image link to set bot pic!</i>"
        ).format(MemoryDB.bot_data.get("bot_pic"))
    
    elif query_data == "images":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "images",
            "is_list": True,
            "is_int": False
        })

        images = MemoryDB.bot_data.get("images")
        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Images (link): <code>{}</code>\n\n"
            "<i><b>Note:</b> Multiple links should be separated by comma.</i>"
        ).format(len(images or []))

        if images:
            await query.answer("Sending images links...")

            with open("temp/images.txt", "w") as f:
                f.write("\n".join(images))
            
            with open("temp/images.txt", "rb") as f:
                images_binary = f.read()
        
            await context.bot.send_document(user.id, images_binary, f"Total images: {len(images)}", filename="images.txt")
    
    elif query_data == "support_chat":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "support_chat",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Support Chat (link): <code>{}</code>\n"
            "<i><b>Note:</b> Group chat link for bot support (optional)</i>"
        ).format(MemoryDB.bot_data.get("support_chat"))
    
    elif query_data == "server_url":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "server_url",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Server URL: <code>{}</code>\n\n"
            "<i><b>Note:</b> If <code>Server URL</code> isn't provided and bot is deployed on render (free) then bot will fall asleep. (Server Reboot Required)</i>"
        ).format(MemoryDB.bot_data.get("server_url"))

    elif query_data == "sudo":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "sudo_users",
            "is_list": True,
            "is_int": True
        })

        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Sudo users: <code>{}</code>\n\n"
            "<i><b>Note: (Warning)</b> Sudo users have owner functions access!\nAdd UserID eg. <code>2134776547</code>\nMultiple ID should be separated by comma.</i>"
        ).format(", ".join(MemoryDB.bot_data.get("sudo_users") or []))

    elif query_data == "shrinkme_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "shrinkme_api",
            "is_list": False,
            "is_int": False
        })
        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Shrinkme API: <code>{}</code>\n\n"
            "<i><b>Note:</b> This API is for /shorturl command.</i>"
        ).format(MemoryDB.bot_data.get("shrinkme_api"))
    
    elif query_data == "omdb_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "omdb_api",
            "is_list": False,
            "is_int": False
        })
        
        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "OMDB API: <code>{}</code>\n\n"
            "<i><b>Note:</b> This API is for /movie command.</i>"
        ).format(MemoryDB.bot_data.get("omdb_api"))
    
    elif query_data == "weather_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "weather_api",
            "is_list": False,
            "is_int": False
        })
        
        is_editing_btn = True

        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            "Weather API: <code>{}</code>\n\n"
            "<i><b>Note:</b> This API is for /weather command.</i>"
        ).format(MemoryDB.bot_data.get("weather_api"))
    
    elif query_data == "restoredb":
        text = (
            "<u><b>Bot Settings</b></u>\n\n"
            
            "<b>• Restore Database</b>\n"
            "- <i>Delete MongoDB's <code>bot_data</code> and restore from backup in <code>config.env</code></i>\n\n"

            "<b>• Wipe Memory Cache</b>\n"
            "- <i>This will clean memory cache.</i>\n\n"

            "<i><b>Note:</b> Use <code>Restore Database</code> with caution!</i>"
        )

        btn_data = [
            {"Restore Database": "bsettings_restoredb_confirm", "Wipe Memory Cache": "bsettings_wipe_memory"},
            {"Back": "bsettings_menu", "Close": "bsettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "restoredb_confirm":
        await query.answer("Restoring Bot Data...")

        # sending backup files
        bot_data = MemoryDB.bot_data
        # removing unnecessary files
        bot_data.pop("_id", "") # deleteing _id object
        bot_data.pop("bot_commands", "")
        bot_data.pop("bot_uptime", "")

        with open("temp/backup_database.json", "w") as f:
            json.dump(bot_data, f, indent=4)
        
        with open("temp/backup_database.json", "rb") as f:
            db_backup = f.read()
        
        await context.bot.send_document(
            user.id,
            db_backup,
            "Database Backup File",
            filename="backup_database.json"
        )

        # process of deleting...
        response = MongoDB.delete_collection("bot_data")
        if response:
            update_database()
            text = "Database has been restored successfully from <code>config.env</code>"
        else:
            text = "Something went wrong! Check /log"
        
        await context.bot.send_message(user.id, text)
        return # don't want to edit message by global reply
    
    elif query_data == "wipe_memory":
        await query.answer("Cleaning Memory Cache...")

        MemoryDB.clear_all()
        update_database()

        await context.bot.send_message(user.id, "Memory Cache has been cleaned!")
        return # don't want to edit message by global reply
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(user.id, [message_id, message_id - 1])
        except:
            pass
        return # don't want to edit message by global reply
    
    # common editing keyboard buttons
    if is_editing_btn:
        btn_data = [
            {"Edit Value": "database_edit_value"},
            {"Remove Value": "database_rm_value"},
            {"Back": "bsettings_menu", "Close": "bsettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    # global reply
    if is_caption:
        await query.edit_message_caption(text, reply_markup=btn)
    else:
        await query.edit_message_text(text, reply_markup=btn)
