import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

async def query_db_editing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("database_")

    # memory access
    data_center = MemoryDB.data_center.get(chat.id) # using chat_id bcz it could be chat settings too
    if not data_center:
        await query.answer("Session Expired.")
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(chat.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return
    
    # verifying user
    user_id = data_center.get("user_id")
    if user_id != user.id:
        await query.answer("Access Denied!", True)
        return
    
    # memory accessed data
    collection_name = data_center.get("collection_name")
    search_key = data_center.get("search_key")
    match_value = data_center.get("match_value")
    update_data_key = data_center.get("update_data_key")
    is_list = data_center.get("is_list") # type of update_data_key
    is_int = data_center.get("is_int") # type of update_data_key
    update_data_value = None # this can't be False/None or any empty value

    # getting update_data_value
    if query_data == "edit_value":
        MemoryDB.insert("data_center", chat.id, {"is_editing": True})
        
        btn = ButtonMaker.cbutton([{"Cancel": "database_cancel_editing"}])
        sent_message = await context.bot.send_message(chat.id, "Waiting for a new value:", reply_markup=btn)

        for i in range(10):
            data_center = MemoryDB.data_center[chat.id]
            # to check > is operation cancelled
            is_editing = data_center.get("is_editing")
            if not is_editing:
                await query.answer()
                return
            
            await asyncio.sleep(1)
            update_data_value = data_center.get("update_data_value")
            if update_data_value:
                break
        
        try:
            message_ids = [sent_message.id]
            if data_center.get("message_id"):
                message_ids.append(data_center.get("message_id"))
            
            await context.bot.delete_messages(chat.id, message_ids)
        except:
            pass

        # terminating editing mode
        MemoryDB.insert("data_center", chat.id, {"update_data_value": None, "is_editing": False})

        if not update_data_value:
            await query.answer("Timeout.")
            return
        
        if is_list:
            values = str(update_data_value).split(",") if "," in str(update_data_value) else [str(update_data_value)]
            update_data_value = [int(v) if is_int else v.strip() for v in values]
        
        # Updating Database
        response = MongoDB.update(collection_name, search_key, match_value, update_data_key, update_data_value)
        if response:
            mem_coll_names = {
                "bot_data": "bot_data",
                "users": "user_data",
                "groups": "chat_data"
            }
            # bcz there are naming diff between mongodb and memory
            collection_name = mem_coll_names[collection_name]
            identifier = None if collection_name == "bot_data" else chat.id
            data = {update_data_key: update_data_value}

            MemoryDB.insert(collection_name, identifier, data)

            await query.answer("Database Updated Successfully.")

        else:
            await query.answer("Something went wrong.")
    
    elif query_data == "cancel_editing":
        MemoryDB.insert("data_center", chat.id, {"update_data_value": None, "is_editing": False})
        await query.answer("Operation cancelled.")
        try:
            await query.delete_message()
        except:
            pass
    
    elif query_data.startswith("value"): # expecting value_ > a fixed value which is update_data_value
        # Updating Database
        update_data_value = query_data.removeprefix("value_")
        response = MongoDB.update(collection_name, search_key, match_value, update_data_key, update_data_value)
        if response:
            mem_coll_names = {
                "bot_data": "bot_data",
                "users": "user_data",
                "groups": "chat_data"
            }
            # bcz there are naming diff between mongodb and memory
            collection_name = mem_coll_names[collection_name]
            identifier = None if collection_name == "bot_data" else chat.id
            data = {update_data_key: update_data_value}

            MemoryDB.insert(collection_name, identifier, data)

            await query.answer("Database Updated Successfully.")

        else:
            await query.answer("Something went wrong.")
    
    elif query_data == "rm_value":
        # Updating Database (removing values)
        update_data_value = [] if is_list else update_data_value
        response = MongoDB.update(collection_name, search_key, match_value, update_data_key, update_data_value)
        if response:
            mem_coll_names = {
                "bot_data": "bot_data",
                "users": "user_data",
                "groups": "chat_data"
            }
            # bcz there are naming diff between mongodb and memory
            collection_name = mem_coll_names[collection_name]
            identifier = None if collection_name == "bot_data" else chat.id
            data = {update_data_key: update_data_value}

            MemoryDB.insert(collection_name, identifier, data)

            await query.answer("Database Updated Successfully.")

        else:
            await query.answer("Something went wrong.")
    
    elif query_data.startswith("bool"): # expecting bool_true or bool_false
        # Updating Database (boolean)
        update_data_value = query_data.strip("bool_") == "true"
        response = MongoDB.update(collection_name, search_key, match_value, update_data_key, update_data_value)
        if response:
            mem_coll_names = {
                "bot_data": "bot_data",
                "users": "user_data",
                "groups": "chat_data"
            }
            # bcz there are naming diff between mongodb and memory
            collection_name = mem_coll_names[collection_name]
            identifier = None if collection_name == "bot_data" else chat.id
            data = {update_data_key: update_data_value}

            MemoryDB.insert(collection_name, identifier, data)

            await query.answer("Database Updated Successfully.")

        else:
            await query.answer("Something went wrong.")
