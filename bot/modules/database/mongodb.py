from pymongo import MongoClient
from bot import CONFIG_FILE, logger
from bot.config import load_config

class MongoDatabase:
    def __init__(self):
        ENV_CONFIG = load_config(CONFIG_FILE)
        self.client = MongoClient(ENV_CONFIG["mongodb_uri"]) # full cluster access
        self.database = self.client[ENV_CONFIG["db_name"]] # for only accessing bot database
    

    def insert_single_data(self, collection_name, data):
        """
        `collection_name` example `users` | `data` type: dict
        """
        try:
            collection = self.database[collection_name]
            inserted_data = collection.insert_one(data)
            if not inserted_data.acknowledged:
                logger.error(f"{collection_name} wasn't inserted.")
        except Exception as e:
            logger.error(e)


    def insert_multiple_data(self, collection_name, data):
        """
        `collection_name` example `users` | `data` type: list of dict
        """
        try:
            collection = self.database[collection_name]
            inserted_data = collection.insert_many(data)
            if not inserted_data.acknowledged:
                logger.error(f"{collection_name} wasn't inserted.")
        except Exception as e:
            logger.error(e)

    def find_one(self, collection_name, search, match):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547`\n
        returns `data` | `None`
        """
        try:
            collection = self.database[collection_name]
            document = collection.find_one({search: match})
            if document:
                return document
        except Exception as e:
            logger.error(e)


    def find(self, collection_name, search):
        """
        `collection_name` example `users` | `search` example `user_id`\n
        returns `list` of matched data
        """
        try:
            collection = self.database[collection_name]
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


    def get_data(self, collection_name, data):
        """
        Gets data from single document, which doesn't have multiple documents\n
        `collection_name` example `bot_data` | `data` example `owner_id`\n
        returns `data` | `None`
        """
        try:
            collection = self.database[collection_name]
            documents = collection.find_one()
            doc_data = documents.get(data)
            if doc_data:
                return doc_data
        except Exception as e:
            logger.error(e)


    def update_db(self, collection_name, search, match, update_data_key, update_data_value):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547` |\
        `update_data_key` example `name` | `update_data_value` example `Bishal`
        """
        try:
            collection = self.database[collection_name]
            updated_data = collection.update_one(
                {search: match},
                {"$set": {update_data_key: update_data_value}}
            )
            if not updated_data.acknowledged:
                logger.error(f"{collection_name} wasn't updated.")
        except Exception as e:
            logger.error(e)


    def update_db_remove(self, collection_name, search, match, remove_field_key):
        """
        `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547` |\
        `remove_field_key` example `name`
        """
        try:
            collection = self.database[collection_name]
            updated_data = collection.update_one(
                {search: match},
                {"$unset": {remove_field_key: ""}}
            )
            if not updated_data.acknowledged:
                logger.error(f"{collection_name} wasn't updated.")
        except Exception as e:
            logger.error(e)


    def info_db(self, collection_name=None):
        """
        `collection_name`: optional\n
        returns `dict`
        """
        docs_name = self.database.list_collection_names()
        data_dict = {}
        for collection_name in docs_name:
            doc_stats = self.database.command("collstats", collection_name)
            # stats
            doc_name = collection_name
            doc_count = doc_stats['count']
            doc_size = f"{doc_stats['storageSize'] / (1024 * 1024):.2f} MB"
            doc_acsize = f"{doc_stats['size'] / (1024 * 1024):.2f} MB"

            data_dict.update({doc_name: {"name": doc_name, "quantity": doc_count, "size": doc_size, "acsize": doc_acsize}})
        return data_dict


    def delete_all_doc(self, collection_name):
        """
        delete all data from `collection_name`
        """
        try:
            collection = self.database[collection_name]
            deleted_data = collection.delete_many({})
            if not deleted_data.acknowledged:
                logger.error(f"{collection_name} wasn't deleted.")
                return False
            return True
        except Exception as e:
            logger.error(e)
    

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
