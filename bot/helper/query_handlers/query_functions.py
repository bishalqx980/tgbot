import asyncio
from bot import logger
from telegram import Update
from telegram.ext import ContextTypes
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
            try:
                await query.answer(f"Error: {identifier} wasn't found in data center! Try to send command again!", True)
            except Exception as e:
                logger.error(e)
            return
        
        for i in ["collection_name", "db_find", "db_vlaue", "edit_data_key"]: # edit_data_value will be added below
            data = data_center.get(i)
            if not data:
                try:
                    await query.answer(f"Error: {i} wasn't found in data center! Try to send command again!", True)
                except Exception as e:
                    logger.error(e)
                return
        
        chat_id = data_center.get("chat_id")
        collection_name = data_center.get("collection_name")
        db_find = data_center.get("db_find")
        db_vlaue = data_center.get("db_vlaue")
        edit_data_key = data_center.get("edit_data_key")
        
        if new_value != "default":
            edit_data_value = new_value
        else:
            sent_message = await context.bot.send_message(chat_id, "Now send a value:")

            MemoryDB.insert_data("data_center", identifier, {"is_editing": True})

            for i in range(20):
                data_center = MemoryDB.data_center.get(identifier)
                edit_data_value = data_center.get("edit_data_value")
                edit_data_value_msg_pointer_id = data_center.get("edit_data_value_msg_pointer_id")
                if edit_data_value:
                    break

                await asyncio.sleep(0.5)
            
            MemoryDB.insert_data("data_center", identifier, {"edit_data_value": None, "is_editing": False})
            await context.bot.delete_messages(chat_id, [edit_data_value_msg_pointer_id, sent_msg.id])
            
            if not edit_data_value:
                try:
                    await query.answer("Oops, Timeout...", True)
                except Exception as e:
                    logger.error(e)
                return
            
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
        
        msg = f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}"
        
        if is_list:
            msg = f"Database updated!\n\nData: {edit_data_key}\nValue: {len(edit_data_value)} items..."
        elif not is_int and new_value != None:
            if len(edit_data_value) > 100:
                msg = "Data is too long, can't show! Check on message..."
        
        try:
            await query.answer(msg, True)
        except Exception as e:
            logger.error(e)


    async def query_rm_value(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            try:
                await query.answer(f"Error: {identifier} wasn't found in data center! Try to send command again!", True)
            except Exception as e:
                logger.error(e)
            return
        
        for i in ["collection_name", "db_find", "db_vlaue", "edit_data_key"]: # edit_data_value will be added below
            data = data_center.get(i)
            if not data:
                try:
                    await query.answer(f"Error: {i} wasn't found in data center! Try to send command again!", True)
                except Exception as e:
                    logger.error(e)
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
        
        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_true(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            try:
                await query.answer(f"Error: {identifier} wasn't found in data center! Try to send command again!", True)
            except Exception as e:
                logger.error(e)
            return
        
        for i in ["collection_name", "db_find", "db_vlaue", "edit_data_key"]: # edit_data_value will be added below
            data = data_center.get(i)
            if not data:
                try:
                    await query.answer(f"Error: {i} wasn't found in data center! Try to send command again!", True)
                except Exception as e:
                    logger.error(e)
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

        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_false(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = MemoryDB.data_center.get(identifier)
        if not data_center:
            try:
                await query.answer(f"Error: {identifier} wasn't found in data center! Try to send command again!", True)
            except Exception as e:
                logger.error(e)
            return
        
        for i in ["collection_name", "db_find", "db_vlaue", "edit_data_key"]: # edit_data_value will be added below
            data = data_center.get(i)
            if not data:
                try:
                    await query.answer(f"Error: {i} wasn't found in data center! Try to send command again!", True)
                except Exception as e:
                    logger.error(e)
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

        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_close(update: Update, context: ContextTypes.DEFAULT_TYPE, identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        chat = update.effective_chat
        data_center = MemoryDB.data_center.get(identifier)
        msg_ids = [query.message.message_id - 1]

        if data_center:
            chat_id = data_center.get("chat_id")
            msg_ids.append(data_center.get("del_msg_pointer_id"))
        else:
            chat_id = chat.id
        
        await context.bot.delete_messages(chat_id, msg_ids)

        try:
            await query.delete_message()
        except Exception as e:
            logger.error(e)
