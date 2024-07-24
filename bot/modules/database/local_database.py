import json
from bot import logger, LOCAL_DB

class LOCAL_DATABASE:
    async def create_collection(collection):
        """
        collection_name = db_collection_name eg. (users or docs)
        """
        if not collection:
            logger.error("collection was't given...")
            return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            check_db = load_db.get(collection) # check if collection exist or not
            if check_db:
                logger.info(f"Collection {collection} already exist!")
                return
            
            load_db[collection] = {}
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)

            logger.info(f"Collection {collection} created...")
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def insert_data_direct(collection, data):
        """
        collection = db_collection_name eg. (users or docs)\n
        data = json data {"name": "bishal", "age": 20}\n\n
        It will add or replace/modify existing data...\n
        use >> insert_data instead if you want sub_entry/identifier
        """
        params = [collection, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            
            # bot_docs exception ...
            if data.get("_id"):
                data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            
            load_collection = load_db.get(collection)
            load_collection.update(data)
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)
            
            logger.info(f"{collection} updated in localdb...")
        except Exception as e:
            logger.error(f"Localdb: {e}")


    async def insert_data(collection, identifier, data, sub_collection=None):
        """
        collection = db_collection_name eg. (users or docs)\n
        identifier = unique data name eg. user.id or doc_1\n
        data = json data {"name": "bishal", "age": 20}\n
        sub_collection = db_sub_collection_name (collection > sub_collection)\n\n
        It will add or replace/modify existing data...
        """
        params = [collection, identifier, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return

        try:
            load_db = json.load(open(LOCAL_DB, "r"))

            # exception ...
            if data.get("_id"):
                data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            
            load_collection = load_db.get(collection, {})
            is_identifier = load_collection.setdefault(str(identifier), {})

            # sub_collection is under identifier ...
            if sub_collection:
                is_sub_collection = is_identifier.setdefault(str(sub_collection), {})
                is_sub_collection.update(data)
            else:
                is_identifier.update(data)
            
            load_db[collection] = load_collection
            json.dump(load_db, open(LOCAL_DB, "w"), indent=4)
            
            if sub_collection:
                logger.info(f"{sub_collection} has been updated in localdb...! Collection: {collection} Identifier: {identifier} ")
            else:
                logger.info(f"{identifier} has been updated in localdb...! Collection: {collection}")
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def find(collection):
        """
        collection = db_collection_name eg. (users or docs)
        """
        if not collection:
            logger.error("collection was't given...")
            return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            load_collection = load_db.get(collection)
            return load_collection
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def find_one(collection, find):
        """
        collection = db_collection_name eg. (users or docs)\n
        find = identifier >> unique data name eg. user_1 or doc_1
        """
        params = [collection, find]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            load_collection = load_db.get(collection)
            data = load_collection.get(str(find))
            return data
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def get_data(collection, data):
        """
        collection = db_collection_name eg. (users or docs)\n
        data = which data you want from specified collection\n
        only works for which doesn't have sub collection
        """
        params = [collection, data]
        for i in params:
            if not i:
                logger.error(f"Some required parameter was't given...")
                return
        
        try:
            load_db = json.load(open(LOCAL_DB, "r"))
            load_collection = load_db.get(collection)
            db_data = load_collection[data]
            return db_data
        except Exception as e:
            logger.error(f"Localdb: {e}")
