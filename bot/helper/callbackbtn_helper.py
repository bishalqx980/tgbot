import asyncio
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.update_db import update_database
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query # always updates whenever clicked a button
    user = update.effective_user
    chat = update.effective_chat

    async def popup(msg):
        await query.answer(msg, True)
    
    async def query_del():
        try:
            await query_del()
        except Exception as e:
            logger.error(e)
    
    async def _update_localdb(collection_name, db_find, db_vlaue):
        """
        collection_name >> eg. users, groups
        db_find >> data to find user_id, username
        db_value >> the data to match
        """
        chat_data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        await LOCAL_DATABASE.insert_data(collection_name, chat.id, chat_data) # common is chat.id for private chat & groups

    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if not data_center:
        await popup("Error: data not found in data center!")
        await query_del()
        return
    
    if chat.type != "private":
        user_id = data_center.get("user_id")
        if user.id != user_id:
            await popup("Access Denied!")
            return


    if query.data in ["query_edit_value", "query_rm_value", "bool_true", "bool_false", "query_close"]:
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")

        for i in [chat_id, collection_name, db_find, db_vlaue, edit_data_key]:
            if not i:
                await popup(f"{i} not found in data center...")
                await query_del()
                return
        
        if query.data == "query_edit_value":
            """
            chat_id --> main
            collection_name --> main / query data
            db_find --> main / query data
            db_vlaue --> main / query data
            edit_data_key --> from query data
            edit_data_value --> from user
            del_msg_pointer -- optional
            edit_data_value_msg_pointer -- optional
            """
            del_msg_1 = await Message.send_msg(chat_id, "Now send a value:")
            data_center["status"] = "editing"
            await asyncio.sleep(1)

            attempt = 0

            while attempt < 20:
                edit_data_value = data_center.get("edit_data_value")
                attempt += 1
                await asyncio.sleep(0.5)
                if edit_data_value:
                    break

            data_center["edit_data_value"] = None

            if not edit_data_value:
                await popup("Timeout!")
                return
            
            del_msg_2 = data_center.get("edit_value_del_msg_pointer")
            del_msg = [del_msg_2, del_msg_1]
            for delete in del_msg:
                await Message.del_msg(chat_id, delete)
            
            # ------------------------------------------------ some exceptions
            
            if edit_data_key in ["images", "allowed_links", "sudo_users"]:
                if "," in str(edit_data_value):
                    storage = []
                    for value in edit_data_value.split(","):
                        if edit_data_key in ["sudo_users"]: # int value
                            storage.append(int(value))
                        else:
                            storage.append(value)
                    edit_data_value = storage
                else:
                    if edit_data_key in ["sudo_users"]: # int value
                        edit_data_value = [int(edit_data_value)]
                    else:
                        edit_data_value = [edit_data_value]
            
            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

                if edit_data_key in ["images", "allowed_links"]:
                    edit_data_value = f"{len(edit_data_value)} items"
                elif edit_data_key == "custom_welcome_msg":
                    edit_data_value = "Check in message..."
                
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "query_rm_value":
            """
            chat_id --> main
            collection_name --> main / query data
            db_find --> main / query data
            db_vlaue --> main / query data
            edit_data_key --> from query data
            """
            edit_data_value = None
            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "bool_true":
            """
            chat_id --> main
            collection_name --> main / query data
            db_find --> main / query data
            db_vlaue --> main / query data
            edit_data_key --> from query data
            """
            edit_data_value = True
            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "bool_false":
            """
            chat_id --> main
            collection_name --> main / query data
            db_find --> main / query data
            db_vlaue --> main / query data
            edit_data_key --> from query data
            """
            edit_data_value = False
            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")

        elif query.data == "query_close":
            chat_id = data_center.get("chat_id")
            del_msg_pointer = data_center.get("del_msg_pointer")

            await query_del()
            await Message.del_msg(chat_id, del_msg_pointer)

    elif chat.type == "private":
        if query.data == "mp4":
            data_center["youtube_content_format"] = query.data

        elif query.data == "mp3":
            data_center["youtube_content_format"] = query.data
        
        elif query.data == "group_management":
            msg = ()

            btn_name = ["Back", "Close"]
            btn_data = ["help_menu", "query_close"]
            btn = await Button.cbutton(btn_name, btn_data, True)

            await Message.edit_msg(update, msg, query.message, btn)
    
    elif chat.type in ["group", "supergroup"]:
        chat_id = data_center.get("chat_id")
        if not chat_id:
            await popup("Error: chat id not found in data center...")
            await query_del()
            return
        
        if query.data == "unpin_all":
            try:
                await bot.unpin_all_chat_messages(chat_id)
                await Message.send_msg(chat_id, "All pinned messages has been unpinned successfully!")
                await query_del()
            except Exception as e:
                logger.error(e)
        
        
        
        elif query.data == "ai":
            msg = (
                
            )

            btn_name = ["Back", "Close"]
            btn_data = ["help_menu", "close"]
            btn = await Button.cbutton(btn_name, btn_data, True)

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "misc_func":
            msg = (
                
            )

            btn_name = ["Back", "Close"]
            btn_data = ["help_menu", "close"]
            btn = await Button.cbutton(btn_name, btn_data, True)

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "owner_func":
            msg = (
                
            )

            btn_name = ["Back", "Close"]
            btn_data = ["help_menu", "close"]
            btn = await Button.cbutton(btn_name, btn_data, True)

            await Message.edit_msg(update, msg, query.message, btn)

        elif query.data == "help_menu":
            db = await MongoDB.info_db()
            for i in db:
                if i[0] == "users":
                    total_users = i[1]
                    break
                else:
                    total_users = "❓"
            
            active_status = await MongoDB.find("users", "active_status")
            active_users = active_status.count(True)
            inactive_users = active_status.count(False)

            msg = ()

            btn_name_row1 = ["Group Management", "Artificial intelligence"]
            btn_data_row1 = ["group_management", "ai"]

            btn_name_row2 = ["misc", "Bot owner"]
            btn_data_row2 = ["misc_func", "owner_func"]

            btn_name_row3 = ["GitHub", "Close"]
            btn_data_row3 = ["github_stats", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

            btn = row1 + row2 + row3

            await Message.edit_msg(update, msg, query.message, btn)
        # ---------------------------------------------------------------------------- help ends
        # bot settings ------------------------------------------------------------- bsettings starts
        elif query.data == "bot_pic":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            bot_pic = await MongoDB.get_data(collection_name, "bot_pic")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "bot_pic"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "welcome_img":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            welcome_img = await MongoDB.get_data(collection_name, "welcome_img")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "welcome_img"
            
            msg = (
                
            )

            btn_name_row1 = ["Yes", "No"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "images":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            images = await MongoDB.get_data(collection_name, "images")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "images"

            if images:
                if len(images) > 20:
                    storage, counter = "", 0
                    for image in images:
                        storage += f"{image},"
                        counter += 1
                        if counter == 20:
                            await Message.send_msg(user.id, f"{storage}")
                            storage, counter = "", 0
                    await Message.send_msg(user.id, f"{storage}")
                    images = "Value sent below!"
                else:
                    storage, counter = "", 0
                    for i in images:
                        counter += 1
                        if counter == len(images):
                            storage += f"{i}"
                        else:
                            storage += f"{i}, "
                    images = storage
            
            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "support_chat":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            support_chat = await MongoDB.get_data(collection_name, "support_chat")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "support_chat"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "server_url":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            server_url = await MongoDB.get_data(collection_name, "server_url")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "server_url"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "sudo_users":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            sudo_users = await MongoDB.get_data(collection_name, "sudo_users")
            if sudo_users:
                storage, counter = "", 0
                for i in sudo_users:
                    counter += 1
                    if counter == len(sudo_users):
                        storage += f"{i}"
                    else:
                        storage += f"{i}, "
                sudo_users = storage

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "sudo_users"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "shrinkme_api":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            shrinkme_api = await MongoDB.get_data(collection_name, "shrinkme_api")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "shrinkme_api"

            msg = (
            
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "omdb_api":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            omdb_api = await MongoDB.get_data(collection_name, "omdb_api")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "omdb_api"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "weather_api":
            collection_name = "bot_docs"
            db_find = "_id"
            db_vlaue = await MongoDB.find(collection_name, db_find)
            weather_api = await MongoDB.get_data(collection_name, "weather_api")

            data_center["collection_name"] = collection_name
            data_center["db_find"] = db_find
            data_center["db_vlaue"] = db_vlaue[0]
            data_center["edit_data_key"] = "weather_api"

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        

        
        elif query.data == "restore_db":
            msg = (
                
            )

            btn_name_row1 = ["⚠ Restore Database"]
            btn_data_row1 = ["confirm_restore_db"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["b_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "confirm_restore_db":
            chat_id = data_center.get("chat_id")
            if not chat_id:
                await popup("Error: chat_id not found!")
                await query_del()
                return

            await MongoDB.delete_all_doc("bot_docs")

            res = await update_database()
            _id = await MongoDB.find("bot_docs", "_id")
            bot_docs = await MongoDB.find_one("bot_docs", "_id", _id[0])
            await LOCAL_DATABASE.insert_data_direct("bot_docs", bot_docs)

            msg = "Database data has been restored successfully from <code>config.env</code>!" if res else "Oops, something went wrong..."
            await Message.send_msg(chat_id, msg)

        elif query.data == "b_setting_menu":
            btn_name_row1 = ["Bot pic", "Welcome img"]
            btn_data_row1 = ["bot_pic", "welcome_img"]

            btn_name_row2 = ["Images", "Support chat"]
            btn_data_row2 = ["images", "support_chat"]

            btn_name_row3 = ["GitHub", "Server url", "Sudo"]
            btn_data_row3 = ["github_repo", "server_url", "sudo_users"]

            btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
            btn_data_row4 = ["shrinkme_api", "omdb_api", "weather_api"]

            btn_name_row5 = ["⚠ Restore Settings", "Close"]
            btn_data_row5 = ["restore_db", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
            row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

            btn = row1 + row2 + row3 + row4 + row5
            
            await Message.edit_msg(update, "<u><b>Bot Settings</b></u>", query.message, btn)
        # ---------------------------------------------------------------------------- bsettings ends
        # chat setting -------------------------------------------------------------- Chat settings starts
        elif query.data == "lang":
            
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return
            
            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            find_chat = await LOCAL_DATABASE.find_one(collection_name, chat.id)
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    await LOCAL_DATABASE.insert_data(collection_name, chat.id, find_chat)
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            lang = find_chat.get("lang")
            data_center["edit_data_key"] = "lang"

            msg = (
                
            )

            btn_name_row1 = ["Language code's"]
            btn_url_row1 = ["https://telegra.ph/Language-Code-12-24"]

            btn_name_row2 = ["Edit Value"]
            btn_data_row2 = ["edit_value"]

            btn_name_row3 = ["Back", "Close"]
            btn_data_row3 = ["c_setting_menu", "close"]

            row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

            btn = row1 + row2 + row3

            await Message.edit_msg(update, msg, query.message, btn)

        elif query.data == "auto_tr":
            
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            auto_tr = find_chat.get("auto_tr")

            data_center["edit_data_key"] = "auto_tr"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)

        elif query.data == "set_echo":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            echo = find_chat.get("echo")

            data_center["edit_data_key"] = "echo"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "welcome_msg":
            
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            welcome_msg = find_chat.get("welcome_msg")

            data_center["edit_data_key"] = "welcome_msg"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Set custom message"]
            btn_data_row2 = ["set_custom_msg"]

            btn_name_row3 = ["Back", "Close"]
            btn_data_row3 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

            btn = row1 + row2 + row3

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "set_custom_msg":
            
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            custom_welcome_msg = find_chat.get("custom_welcome_msg")

            data_center["edit_data_key"] = "custom_welcome_msg"

            msg = (
                
            )

            btn_name_row1 = ["Set default message", "Set custom message"]
            btn_data_row1 = ["remove_value", "edit_value"]

            btn_name_row2 = ["Text formatting"]
            btn_data_row2 = ["text_formats"]

            btn_name_row3 = ["Back", "Close"]
            btn_data_row3 = ["welcome_msg", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

            btn = row1 + row2 + row3

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "text_formats":
            chat_id = data_center.get("chat_id")
            if not chat_id:
                await popup("Error: chat_id not found!")
                await query_del()
                return
            
            msg = (
                
            )

            btn_name = ["Close"]
            btn_data = ["close"]
            
            btn = await Button.cbutton(btn_name, btn_data)
            
            await Message.send_msg(chat_id, msg, btn)

        elif query.data == "goodbye_msg":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            goodbye_msg = find_chat.get("goodbye_msg")

            data_center["edit_data_key"] = "goodbye_msg"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)

        elif query.data == "antibot":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            antibot = find_chat.get("antibot")

            data_center["edit_data_key"] = "antibot"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "del_cmd":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = await LOCAL_DATABASE.find_one(collection_name, chat.id)
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            del_cmd = find_chat.get("del_cmd")

            data_center["edit_data_key"] = "del_cmd"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "log_channel":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            data_center["edit_data_key"] = "log_channel"

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            log_channel = find_chat.get("log_channel")

            msg = (
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "links_behave":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
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
                
            )

            btn_name_row1 = ["All links", "Allowed links"]
            btn_data_row1 = ["all_links", "allowed_links"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)

        elif query.data == "all_links":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            data_center["edit_data_key"] = "all_links"

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            all_links = find_chat.get("all_links")

            msg = (
                
            )

            btn_name_row1 = ["Delete", "Convert", "Nothing"]
            btn_data_row1 = ["d_links", "c_links", "none_links"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["links_behave", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "allowed_links":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            data_center["edit_data_key"] = "allowed_links"

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
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
                
            )

            btn_name_row1 = ["Edit Value", "Remove Value"]
            btn_data_row1 = ["edit_value", "remove_value"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["links_behave", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "d_links":
            chat_id = data_center.get("chat_id")
            if not chat_id:
                await popup("Error: chat_id not found!")
                await query_del()
                return
            
            collection_name = data_center.get("collection_name") # set from main.py
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return
            
            db_find = data_center.get("db_find") # set from main.py
            db_vlaue = data_center.get("db_vlaue") # set from main.py
            edit_data_key = data_center.get("edit_data_key") # set from query data
            edit_data_value = "delete"

            if not edit_data_key:
                await popup("I don't know which data to update! Please go back and then try again!")
                return

            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "c_links":
            chat_id = data_center.get("chat_id")
            if not chat_id:
                await popup("Error: chat_id not found!")
                await query_del()
                return
            
            collection_name = data_center.get("collection_name") # set from main.py
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return
            
            db_find = data_center.get("db_find") # set from main.py
            db_vlaue = data_center.get("db_vlaue") # set from main.py
            edit_data_key = data_center.get("edit_data_key") # set from query data
            edit_data_value = "convert"

            if not edit_data_key:
                await popup("I don't know which data to update! Please go back and then try again!")
                return

            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "none_links":
            chat_id = data_center.get("chat_id")
            if not chat_id:
                await popup("Error: chat_id not found!")
                await query_del()
                return
            
            collection_name = data_center.get("collection_name") # set from main.py
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return
            
            db_find = data_center.get("db_find") # set from main.py
            db_vlaue = data_center.get("db_vlaue") # set from main.py
            edit_data_key = data_center.get("edit_data_key") # set from query data
            edit_data_value = None

            if not edit_data_key:
                await popup("I don't know which data to update! Please go back and then try again!")
                return

            try:
                await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)
                await popup(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}")
                await _update_localdb(collection_name, db_find, db_vlaue)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat_id, f"Error: {e}")
        
        elif query.data == "ai_status":
            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return

            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")

            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            ai_status = find_chat.get("ai_status")

            data_center["edit_data_key"] = "ai_status"

            msg = (
                
            )

            btn_name_row1 = ["Enable", "Disable"]
            btn_data_row1 = ["true", "false"]

            btn_name_row2 = ["Back", "Close"]
            btn_data_row2 = ["c_setting_menu", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2

            await Message.edit_msg(update, msg, query.message, btn)
        
        elif query.data == "c_setting_menu":

            collection_name = data_center.get("collection_name")
            if not collection_name:
                await popup("An error occurred! send command again then try...")
                await query_del()
                return
            
            db_find = data_center.get("db_find")
            db_vlaue = data_center.get("db_vlaue")
            
            try:
                find_chat = data_center[collection_name]
            except Exception as e:
                logger.error(e)
                find_chat = None
            
            if not find_chat:
                find_chat = await MongoDB.find_one(collection_name, db_find, db_vlaue)
                if find_chat:
                    data_center[collection_name] = find_chat
                else:
                    await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    await query_del()
                    return
            
            if collection_name == "db_group_data":
                title = find_chat.get("title")
                lang = find_chat.get("lang")

                echo = find_chat.get("echo")
                auto_tr = find_chat.get("auto_tr")
                welcome_msg = find_chat.get("welcome_msg")
                goodbye_msg = find_chat.get("goodbye_msg")
                antibot = find_chat.get("antibot")
                ai_status = find_chat.get("ai_status")
                del_cmd = find_chat.get("del_cmd")
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

                log_channel = find_chat.get("log_channel")

                msg = (
                    
                )

                btn_name_row1 = ["Language", "Auto translate"]
                btn_data_row1 = ["lang", "auto_tr"]

                btn_name_row2 = ["Echo", "Anti bot"]
                btn_data_row2 = ["set_echo", "antibot"]

                btn_name_row3 = ["Welcome", "Goodbye"]
                btn_data_row3 = ["welcome_msg", "goodbye_msg"]

                btn_name_row4 = ["Delete cmd", "Log channel"]
                btn_data_row4 = ["del_cmd", "log_channel"]

                btn_name_row5 = ["Links", "AI"]
                btn_data_row5 = ["links_behave", "ai_status"]

                btn_name_row6 = ["Close"]
                btn_data_row6 = ["close"]

                row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
                row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
                row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
                row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
                row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
                row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

                btn = row1 + row2 + row3 + row4 + row5 + row6

            elif collection_name == "db_user_data":
                user_mention = find_chat.get("mention")
                lang = find_chat.get("lang")
                echo = find_chat.get("echo")
                auto_tr = find_chat.get("auto_tr")

                msg = ()

                btn_name_row1 = ["Language", "Auto translate"]
                btn_data_row1 = ["lang", "auto_tr"]

                btn_name_row2 = ["Echo", "Close"]
                btn_data_row2 = ["set_echo", "close"]

                row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
                row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                btn = row1 + row2

            else:
                await query_del()
                return
            
            await Message.edit_msg(update, msg, query.message, btn)
