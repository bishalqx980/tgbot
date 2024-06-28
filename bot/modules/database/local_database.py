import json
from bot import logger, LOCAL_DB

class LOCAL_DATABASE:
    async def create_collection(collection):
        """
        collection_name = db_collection_name eg. (users or docs)
        """
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            check_db = load_db.get(collection) # check if collection exist or not
            if check_db:
                logger.info(f"Collection {collection} already exist!")
                return
            
            load_db[collection] = {}

            with open(LOCAL_DB, "w") as f:
                json.dump(load_db, f, indent=4)
            
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
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            # bot_docs exception ...
            if data.get("_id"):
                data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            
            load_collection = load_db.get(collection)
            load_collection.update(data)

            with open(LOCAL_DB, "w") as f:
                json.dump(load_db, f, indent=4)
            
            logger.info(f"{collection} updated in localdb...")
        except Exception as e:
            logger.error(f"Localdb: {e}")


    async def insert_data(collection, identifier, data):
        """
        collection = db_collection_name eg. (users or docs)\n
        identifier = unique data name eg. user_1 or doc_1\n
        data = json data {"name": "bishal", "age": 20}\n\n
        It will add or replace/modify existing data...
        """
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            load_collection = load_db.get(collection)
            check_db = load_collection.get(str(identifier))
            if load_collection:
                load_identifier = load_collection.get(str(identifier))
                load_identifier.update(data)
            else:
                load_collection[str(identifier)] = data

            with open(LOCAL_DB, "w") as f:
                json.dump(load_db, f, indent=4)
            
            if check_db:
                logger.info(f"{identifier} updated in collection {collection} in localdb...")
            else:
                logger.info(f"{identifier} created in collection {collection} in localdb...")
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def find(collection):
        """
        collection = db_collection_name eg. (users or docs)
        """
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            load_collection = load_db.get(collection)
            return load_collection
        except Exception as e:
            logger.error(f"Localdb: {e}")
    

    async def find_one(collection, find):
        """
        collection = db_collection_name eg. (users or docs)\n
        find = identifier >> unique data name eg. user_1 or doc_1
        """
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
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
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            load_collection = load_db.get(collection)
            db_data = load_collection[data]
            return db_data
        except Exception as e:
            logger.error(f"Localdb: {e}")
