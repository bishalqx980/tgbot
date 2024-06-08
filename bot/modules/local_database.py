import os
import json
from bot import logger

LOCAL_DB = "database.json"

check_path = os.path.isfile(LOCAL_DB)
if check_path:
    try:
        with open(LOCAL_DB, "r") as f:
            localdb_data = json.load(f)

        if not all(key in localdb_data for key in ("bot_docs", "users", "groups")):
            check_path = None
    except Exception as e:
        check_path = None
        logger.error(e)

if not check_path:
    logger.info(f"Local Database: {LOCAL_DB} not found...")
    try:
        with open(LOCAL_DB, "w") as f:
            data = {"bot_docs": {}, "users": {}, "groups": {}}
            json.dump(data, f, indent=4)
            logger.info(f"Local Database: {LOCAL_DB} created...")
    except Exception as e:
        logger.error(e)


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
            logger.error(e)
    

    async def insert_data_direct(collection, data):
        """
        collection = db_collection_name eg. (users or docs)\n
        data = json data {"name": "bishal", "age": 20}\n\n
        It will add or replace/modify existing data...
        use >> insert_data instead if you want sub_entry/identifier
        """
        try:
            with open(LOCAL_DB, "r") as f:
                load_db = json.load(f)
            
            data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            load_collection = load_db.get(collection)
            load_collection.update(data)

            with open(LOCAL_DB, "w") as f:
                json.dump(load_db, f, indent=4)
            
            logger.info(f"Database: {collection} updated!")
        except Exception as e:
            logger.error(e)


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
            
            data["_id"] = str(data["_id"]) # mongodb _id >> make it str
            load_collection = load_db.get(collection)
            check_db = load_collection.get(str(identifier))
            load_collection[str(identifier)] = data

            with open(LOCAL_DB, "w") as f:
                json.dump(load_db, f, indent=4)
            
            if check_db:
                logger.info(f"Database: {identifier} updated!")
            else:
                logger.info(f"Entry: {identifier} created...")
        except Exception as e:
            logger.error(e)
    

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
            logger.error(e)
    

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
            logger.error(e)
