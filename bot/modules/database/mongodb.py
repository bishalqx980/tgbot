from pymongo import MongoClient
from bot import mongodb_uri, db_name, logger

# connecting to db
client = MongoClient(mongodb_uri) # full cluster access
db = client[db_name] # for only accessing bot database

class MongoDB:
    @staticmethod
    async def insert_single_data(collection_name, data):
        """
        `collection_name` example `users` | `data` type: dict
        """
        try:
            collection = db[collection_name]
            inserted_data = collection.insert_one(data)
            if not inserted_data.acknowledged:
                logger.error(f"{collection_name} wasn't inserted.")
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def insert_multiple_data(collection_name, data):
        """
        `collection_name` example `users` | `data` type: list of dict
        """
        try:
            collection = db[collection_name]
            inserted_data = collection.insert_many(data)
            if not inserted_data.acknowledged:
                logger.error(f"{collection_name} wasn't inserted.")
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def find_one(collection_name, search, match):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547`\n
        returns `data` | `None`
        """
        try:
            collection = db[collection_name]
            document = collection.find_one({search: match})
            if document:
                return document
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def find(collection_name, search):
        """
        `collection_name` example `users` | `search` example `user_id`\n
        returns `list` of matched data
        """
        try:
            collection = db[collection_name]
            documents = collection.find({})
            if not documents:
                return
            
            storage = []
            for document in documents:
                doc_value = document.get(search)
                storage.append(doc_value)
            return storage
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def get_data(collection_name, data):
        """
        Gets data from single document, which doesn't have multiple documents\n
        `collection_name` example `bot_docs` | `data` example `owner_id`\n
        returns `data` | `None`
        """
        try:
            collection = db[collection_name]
            documents = collection.find_one()
            data = documents.get(data)
            if data:
                return data
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def update_db(collection_name, search, match, update_data_key, update_data_value):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547` |\
        `update_data_key` example `name` | `update_data_value` example `Bishal`
        """
        try:
            collection = db[collection_name]
            updated_data = collection.update_one(
                {search: match},
                {"$set": {update_data_key: update_data_value}}
            )
            if not updated_data.acknowledged:
                logger.error(f"{collection_name} wasn't updated.")
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def update_db_remove(collection_name, search, match, remove_field_key):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547` |\
        `remove_field_key` example `name`
        """
        try:
            collection = db[collection_name]
            updated_data = collection.update_one(
                {search: match},
                {"$unset": {remove_field_key: ""}}
            )
            if not updated_data.acknowledged:
                logger.error(f"{collection_name} wasn't updated.")
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def info_db(collection_name=None):
        """
        Get database info or any collection info
        """
        docs_name = db.list_collection_names()
        storage = []
        for collection_name in docs_name:
            doc_stats = db.command("collstats", collection_name)
            # stats
            doc_name = collection_name
            doc_count = doc_stats['count']
            doc_size = f"{doc_stats['storageSize'] / (1024 * 1024):.2f} MB"
            doc_acsize = f"{doc_stats['size'] / (1024 * 1024):.2f} MB"
            storage.append((doc_name, doc_count, doc_size, doc_acsize))
        return storage


    @staticmethod
    async def delete_all_doc(collection_name):
        """
        delete all data from `collection_name`
        """
        try:
            collection = db[collection_name]
            deleted_data = collection.delete_many({})
            if not deleted_data.acknowledged:
                logger.error(f"{collection_name} wasn't deleted.")
                return False
            return True
        except Exception as e:
            logger.error(e)
