import os
import json
from bot import logger, LOCAL_DB

class LOCAL_DATABASE:
    @staticmethod
    async def create_collection(collection_name):
        """
        `collection_name` example `users`\n
        returns `data` | `None`
        """
        if not collection_name:
            logger.error("Collection name was't given.")
            return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            check_db = load_db.get(collection_name) # check if collection exist or not
            if check_db:
                logger.info(f"Collection: {collection_name} already exist!")
                return
            
            load_db[collection_name] = {}
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)

            logger.info(f"Collection: {collection_name} created...")
            return True
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    @staticmethod
    async def insert_data_direct(collection_name, data):
        """
        `collection_name` example `users` | `data` type: dict\n
        Note: It will add new data or replace existing data. Use `insert_data` function if you want sub_entry/identifier\n
        returns `True` | `None`
        """
        params = [collection_name, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            
            # bot_docs exception ...
            if data.get("_id"):
                data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            
            loaded_collection = load_db.get(collection_name)
            loaded_collection.update(data)
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)
            
            logger.info(f"Collection: {collection_name} updated in localdb.")
            return True
        except Exception as e:
            logger.error(f"Localdb: {e}")


    @staticmethod
    async def insert_data(collection_name, identifier, data, sub_collection_name=None):
        """
        `collection_name` example `users` | `identifier` example `2134776547` | `data` type: dict | `sub_collection` name \
        if you want to add sub collection for this collection.

        It will add or replace/modify existing data...\n
        returns `True` | `None`
        """
        params = [collection_name, identifier, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return

        try:
            load_db = json.load(open(LOCAL_DB, "r"))

            # exception ...
            if data.get("_id"):
                data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            
            loaded_collection = load_db.get(collection_name, {})
            is_identifier = loaded_collection.setdefault(str(identifier), {})

            # sub_collection is under identifier ...
            if sub_collection_name:
                is_sub_collection = is_identifier.setdefault(str(sub_collection_name), {})
                is_sub_collection.update(data)
            else:
                is_identifier.update(data)
            
            load_db[collection_name] = loaded_collection
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)
            
            if sub_collection_name:
                logger.info(f"Sub-Collection: {sub_collection_name} has been updated in localdb. Collection: {collection_name} Identifier: {identifier}")
            else:
                logger.info(f"Identifier: {identifier} has been updated in localdb. Collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    @staticmethod
    async def find(collection_name):
        """
        `collection_name` example `users`\n
        returns `data` | `None`
        """
        if not collection_name:
            logger.error("collection_name was't given...")
            return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            loaded_collection = load_db.get(collection_name)
            return loaded_collection
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    @staticmethod
    async def find_one(collection_name, find):
        """
        `collection_name` example `users` | `find` data to find\n
        returns `data` | `None`
        """
        params = [collection_name, find]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            loaded_collection = load_db.get(collection_name)
            data = loaded_collection.get(str(find))
            return data
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    @staticmethod
    async def get_data(collection_name, data):
        """
        `collection_name` example `bot_docs` | `data` example `owner_id`\n
        Note: only works if collection doesn't have any sub collection\n
        returns `data` | `None`
        """
        params = [collection_name, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            loaded_collection = load_db.get(collection_name)
            db_data = loaded_collection[data]
            return db_data
        except Exception as e:
            logger.error(f"Localdb: {e}")


    @staticmethod
    async def restore_db(default_structure):
        """
        `structure`: `dict` format | example `{"bot_docs": {}, "users": {}, "groups": {}, "data_center": {}}`
        returns `True` | `None`
        """
        try:
            # checking file
            check_local_db = os.path.isfile(LOCAL_DB)
            if not check_local_db:
                logger.info("localdb not found...")
                json.dump({}, open(LOCAL_DB, "w"))
                logger.info("localdb created...")
            
            # restore process
            json.dump(
                default_structure,
                open(LOCAL_DB, "w"),
                indent=4
            )
            logger.info("localdb has been restored successfully...")
            return True
        except Exception as e:
            logger.error(f"Localdb: {e}")
