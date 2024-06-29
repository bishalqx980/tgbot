import asyncio
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


class QueryFunctions:
    async def query_edit_value(identifier, query, chat, new_value="default", is_list=bool(False), is_int=bool(False)):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator\n
        new_value > edit_data_value\n
        is_list > new value could be a list?\n
        is_int > new value could be integer?
        """
        data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
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
            sent_msg = await Message.send_msg(chat_id, "Now send a value:")

            await LOCAL_DATABASE.insert_data("data_center", identifier, {"is_editing": True})

            for i in range(20):
                data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
                edit_data_value = data_center.get("edit_data_value")
                edit_data_value_msg_pointer_id = data_center.get("edit_data_value_msg_pointer_id")
                if edit_data_value:
                    break

                await asyncio.sleep(0.5)
            
            await LOCAL_DATABASE.insert_data("data_center", identifier, {"edit_data_value": None, "is_editing": False})
            await Message.del_msg(chat_id, msg_id=edit_data_value_msg_pointer_id)
            await Message.del_msg(chat_id, sent_msg)
            
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
                        if is_int:
                            storage.append(int(value))
                        else:
                            storage.append(value)
                    edit_data_value = storage
                else:
                    if is_int:
                        edit_data_value = [int(edit_data_value)]
                    else:
                        edit_data_value = [edit_data_value]
        
        # bot_docs exception ...
        if db_find == "_id":
            db_vlaue = await MongoDB.find("bot_docs", "_id")
            db_vlaue = db_vlaue[0]
        
        await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        if db_find == "_id":
            await LOCAL_DATABASE.insert_data_direct(collection_name, data)
        else:
            await LOCAL_DATABASE.insert_data(collection_name, chat_id, data)
        
        
        if is_list and len([edit_data_value]) > 5:
            msg = f"{len([edit_data_value])} items"
        elif not is_int and len(edit_data_value) > 100:
            msg = "Data is too long, can't show! Check on message..."
        else:
            msg = f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}"
        
        try:
            await query.answer(msg, True)
        except Exception as e:
            logger.error(e)


    async def query_rm_value(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
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

        # bot_docs exception ...
        if db_find == "_id":
            db_vlaue = await MongoDB.find("bot_docs", "_id")
            db_vlaue = db_vlaue[0]
        
        await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        if db_find == "_id":
            await LOCAL_DATABASE.insert_data_direct(collection_name, data)
        else:
            await LOCAL_DATABASE.insert_data(collection_name, chat_id, data)
        
        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_true(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
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

        # bot_docs exception ...
        if db_find == "_id":
            db_vlaue = await MongoDB.find("bot_docs", "_id")
            db_vlaue = db_vlaue[0]

        await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        if db_find == "_id":
            await LOCAL_DATABASE.insert_data_direct(collection_name, data)
        else:
            await LOCAL_DATABASE.insert_data(collection_name, chat_id, data)

        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_false(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
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

        # bot_docs exception ...
        if db_find == "_id":
            db_vlaue = await MongoDB.find("bot_docs", "_id")
            db_vlaue = db_vlaue[0]

        await MongoDB.update_db(collection_name, db_find, db_vlaue, edit_data_key, edit_data_value)

        data = await MongoDB.find_one(collection_name, db_find, db_vlaue)
        if db_find == "_id":
            await LOCAL_DATABASE.insert_data_direct(collection_name, data)
        else:
            await LOCAL_DATABASE.insert_data(collection_name, chat_id, data)

        try:
            await query.answer(f"Database updated!\n\nData: {edit_data_key}\nValue: {edit_data_value}", True)
        except Exception as e:
            logger.error(e)


    async def query_close(identifier, query):
        """
        identifier > user.id or chat.id (data center identifier)\n
        query > query indicator
        """
        data_center = await LOCAL_DATABASE.find_one("data_center", identifier)
        if not data_center:
            try:
                await query.answer(f"Error: {identifier} wasn't found in data center! Try to send command again!", True)
            except Exception as e:
                logger.error(e)
            return
        
        chat_id = data_center.get("chat_id")
        del_msg_pointer_id = data_center.get("del_msg_pointer_id")

        await Message.del_msg(chat_id, msg_id=del_msg_pointer_id)

        try:
            await query.message.delete()
        except Exception as e:
            logger.error(e)
