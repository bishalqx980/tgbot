import asyncio
from bot import logger
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

class QueryFunctions:
    async def query_edit_value(context: ContextTypes.DEFAULT_TYPE, identifier, query, new_value="default", is_list=False, is_int=False):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator\n
        new_value > edit_data_value\n
        is_list > new value could be a list?\n
        is_int > new value could be integer?
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            await query.delete_message()
            return
        
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")
        
        if new_value != "default": # if value is given
            edit_data_value = new_value
        
        else:
            MemoryDB.insert_data("data_center", identifier, {"is_editing": True})

            text = "Waiting for a new value:"
            btn = ButtonMaker.cbutton([{"Cancel": "query_close"}])
            sent_message = await context.bot.send_message(chat_id, text, reply_markup=btn)

            for i in range(11):
                data_center = MemoryDB.data_center.get(identifier)
                edit_data_value = data_center.get("edit_data_value")
                edit_data_value_msg_pointer_id = data_center.get("edit_data_value_msg_pointer_id")
                if edit_data_value:
                    break
                
                try:
                    await context.bot.edit_message_text(f"{text} ({i}/10)", chat_id, sent_message.id, reply_markup=btn)
                except BadRequest:
                    try:
                        await query.answer("Operation cancelled!", True)
                    except:
                        await context.bot.send_message(chat_id, "Operation cancelled!")
                    return
                
                await asyncio.sleep(1)
            
            MemoryDB.insert_data("data_center", identifier, {"edit_data_value": None, "is_editing": False})

            if not edit_data_value:
                await context.bot.edit_message_text("Oops! Timeout...", chat_id, sent_message.id)
                return
            
            await context.bot.delete_messages(chat_id, [edit_data_value_msg_pointer_id, sent_message.id])

            if is_list:
                if "," in str(edit_data_value):
                    storage = []
                    for value in edit_data_value.split(","):
                        value = int(value) if is_int else value.strip()
                        storage.append(value)
                    edit_data_value = storage
                else:
                    edit_data_value = [int(edit_data_value)] if is_int else [edit_data_value]
                
        # bot_data exception ...
        if db_find == "_id":
            db_vlaue = MongoDB.find("bot_data", "_id")
            db_vlaue = db_vlaue[0]
        
        MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = MongoDB.find_one(collection_name, db_find, db_vlaue)
        mem_collec_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }

        if db_find == "_id":
            MemoryDB.insert_data(mem_collec_names[collection_name], None, data)
        else:
            MemoryDB.insert_data(mem_collec_names[collection_name], chat_id, data)
        
        text = f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}"
        
        if is_list:
            text = f"Database updated!\n\nData: {edit_data_key}\nValue: {len(edit_data_value)} items."
        elif not is_int and new_value != None:
            if len(edit_data_value) > 100:
                text = "Data is too long, can't show! Check on message."
        
        try:
            await query.answer(text, True)
        except:
            await context.bot.send_message(chat_id, text)


    async def query_rm_value(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            await query.delete_message()
            return
        
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")
        edit_data_value = None

        # bot_data exception ...
        if db_find == "_id":
            db_vlaue = MongoDB.find("bot_data", "_id")
            db_vlaue = db_vlaue[0]
        
        MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = MongoDB.find_one(collection_name, db_find, db_vlaue)
        mem_collec_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }

        if db_find == "_id":
            MemoryDB.insert_data(mem_collec_names[collection_name], None, data)
        else:
            MemoryDB.insert_data(mem_collec_names[collection_name], chat_id, data)
        
        await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)


    async def query_true(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            await query.delete_message()
            return
        
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")
        edit_data_value = True

        # bot_data exception ...
        if db_find == "_id":
            db_vlaue = MongoDB.find("bot_data", "_id")
            db_vlaue = db_vlaue[0]

        MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = MongoDB.find_one(collection_name, db_find, db_vlaue)
        mem_collec_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }

        if db_find == "_id":
            MemoryDB.insert_data(mem_collec_names[collection_name], None, data)
        else:
            MemoryDB.insert_data(mem_collec_names[collection_name], chat_id, data)

        await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)


    async def query_false(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            await query.delete_message()
            return
        
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")
        edit_data_value = False

        # bot_data exception ...
        if db_find == "_id":
            db_vlaue = MongoDB.find("bot_data", "_id")
            db_vlaue = db_vlaue[0]

        MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = MongoDB.find_one(collection_name, db_find, db_vlaue)
        mem_collec_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }

        if db_find == "_id":
            MemoryDB.insert_data(mem_collec_names[collection_name], None, data)
        else:
            MemoryDB.insert_data(mem_collec_names[collection_name], chat_id, data)

        await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)


    async def query_close(context: ContextTypes.DEFAULT_TYPE, identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if data_center:
            try:
                await context.bot.delete_message(data_center.get("chat_id"), data_center.get("del_msg_pointer_id"))
            except Exception as e:
                logger.error(e)
        
        try:
            await query.delete_message()
        except Exception as e:
            logger.error(e)
