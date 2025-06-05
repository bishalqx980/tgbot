import json
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot import logger
from bot.update_db import update_database
from bot.helper import BuildKeyboard
from bot.modules.database import MemoryDB, MongoDB
from ..owner_func.bsettings import BotSettingsData

async def query_bot_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("bsettings_")

    # accessing bot_data
    bot_data = MemoryDB.bot_data

    # variable required for global reply
    is_editing_btn = None

    if query_data == "menu":
        text = BotSettingsData.TEXT.format(
            bot_data.get('show_bot_pic') or False,
            len(bot_data.get('images') or []),
            bot_data.get('support_chat'),
            bot_data.get('server_url'),
            len(bot_data.get('sudo_users') or []),
            bot_data.get('shrinkme_api'),
            bot_data.get('omdb_api'),
            bot_data.get('weather_api')
        )

        btn = BuildKeyboard.cbutton(BotSettingsData.BUTTONS)
    
    elif query_data == "show_bot_pic":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "show_bot_pic",
            "is_list": False,
            "is_int": False
        })

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Show Bot Photo: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Send's /start message or other supported message with Bot photo.</blockquote>"
        ).format(bot_data.get("show_bot_pic"))

        btn_data = [
            {"YES": "database_bool_true", "NO": "database_bool_false"},
            {"Back": "bsettings_menu", "Close": "bsettings_close"}
        ]

        btn = BuildKeyboard.cbutton(btn_data)
    
    elif query_data == "images":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "images",
            "is_list": True,
            "is_int": False
        })

        images = bot_data.get("images")
        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Images (link): <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Images that will be randomly shown with various command messages. Multiple links should be separated by comma.</blockquote>"
        ).format(len(images or []))

        if images:
            await query.answer("Sending images links...")

            images_binary = BytesIO(",\n".join(images).encode())
            images_binary.name = "images.txt"

            await context.bot.send_document(user.id, images_binary, f"Total images: {len(images)}")
    
    elif query_data == "support_chat":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "support_chat",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Support Chat (link): <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Group chat link for bot support (optional)</blockquote>"
        ).format(bot_data.get("support_chat"))
    
    elif query_data == "server_url":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "server_url",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Server URL: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> If <code>Server URL</code> isn't provided and bot is deployed on render (free) then bot will fall asleep. (Server Reboot Required)</blockquote>"
        ).format(bot_data.get("server_url"))

    elif query_data == "sudo":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "sudo_users",
            "is_list": True,
            "is_int": True
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Sudo users: <code>{}</code>\n\n"
            "<blockquote><b>Note: (Warning)</b> Sudo users have owner functions access!\nAdd UserID eg. <code>2134776547</code>\nMultiple ID should be separated by comma.</blockquote>"
        ).format(", ".join(str(user_id) for user_id in (bot_data.get("sudo_users") or [])))

    elif query_data == "shrinkme_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "shrinkme_api",
            "is_list": False,
            "is_int": False
        })
        
        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Shrinkme API: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This API is for /shorturl command.</blockquote>"
        ).format(bot_data.get("shrinkme_api"))
    
    elif query_data == "omdb_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "omdb_api",
            "is_list": False,
            "is_int": False
        })
        
        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "OMDB API: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This API is for /movie command.</blockquote>"
        ).format(bot_data.get("omdb_api"))
    
    elif query_data == "weather_api":
        MemoryDB.insert("data_center", user.id, {
            "update_data_key": "weather_api",
            "is_list": False,
            "is_int": False
        })
        
        is_editing_btn = True

        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "Weather API: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This API is for /weather command.</blockquote>"
        ).format(bot_data.get("weather_api"))
    
    elif query_data == "database":
        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "<b>• Restore Database</b>\n"
            "- <i>Delete MongoDB's <code>bot_data</code> and restore from backup in <code>config.env</code></i>\n\n"

            "<b>• Wipe Memory Cache</b>\n"
            "- <i>This will clean memory cache.</i>\n\n"

            "<blockquote><b>Note:</b> Use <code>Restore Database</code> with caution!</blockquote>"
        )

        btn_data = [
            {"Restore Database": "bsettings_restoredb", "Wipe Memory Cache": "bsettings_wipe_memory"},
            {"Back": "bsettings_menu", "Close": "bsettings_close"}
        ]

        btn = BuildKeyboard.cbutton(btn_data)
    
    elif query_data == "restoredb":
        text = (
            "<blockquote><b>Bot Settings</b></blockquote>\n\n"
            "<b>• Restore MongoDB Database?</b>"
        )

        btn_data = [
            {"YES": "bsettings_restoredb_confirm", "NO": "bsettings_database"},
            {"Back": "bsettings_database"}
        ]

        btn = BuildKeyboard.cbutton(btn_data)
    
    elif query_data == "restoredb_confirm":
        await query.answer("Restoring Bot Data...")

        # removing unnecessary files
        bot_data.pop("_id", "") # deleteing _id object
        
        db_backup = BytesIO(json.dumps(bot_data, indent=4).encode())
        db_backup.name = "backup_database.json"

        await context.bot.send_document(
            user.id,
            db_backup,
            "Database Backup File"
        )

        # process of deleting...
        response = MongoDB.delete_collection("bot_data")
        if response:
            bot_data.clear()
            update_database()
            text = (
                "Database has been restored successfully from <code>config.env</code>\n"
                "<blockquote><b>Note:</b> Reboot is recommended.</blockquote>"
            )
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

        btn = BuildKeyboard.cbutton(btn_data)
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
