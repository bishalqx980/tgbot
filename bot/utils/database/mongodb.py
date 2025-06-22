from pymongo import MongoClient
from bot import logger, config

class MongoDatabase:
    def __init__(self):
        self.client = MongoClient(config.mongodb_uri) # full cluster access
        self.database = self.client[config.db_name] # for only accessing bot database
    

    def insert(self, collection_name, data: dict):
        """
        :param collection_name: Example:`MongoDatabase.BOT_DATA`
        :param data: `dict` if data
        :return bool: `True` | `False` | `None`
        """
        try:
            coll_data = self.database[collection_name]
            response = coll_data.insert_one(data)

            return response.acknowledged
        except Exception as e:
            logger.error(e)


    def find_one(self, collection_name, search_key, match_value):
        """
        :param collection_name: Example:`MongoDatabase.USERS_DATA`
        :param search_key: Key to search. e.g. `user_id`
        :param match_value: Value to match. e.g. `2134776547`
        :return dict: Speficied search data | `None`
        """
        try:
            coll_data = self.database[collection_name]
            document = coll_data.find_one({search_key: match_value})

            return document
        except Exception as e:
            logger.error(e)


    def find(self, collection_name, search_key):
        """
        :param collection_name: Example:`MongoDatabase.USERS_DATA`
        :param search_key: Key to search. e.g. `user_id`
        :return list: Value `list` of speficied search key | `None`
        """
        try:
            coll_data = self.database[collection_name]
            documents = coll_data.find({})
            storage = []

            for doc in documents:
                doc_value = doc.get(search_key)
                storage.append(doc_value)
            
            return storage
        except Exception as e:
            logger.error(e)


    def get(self, collection_name, key):
        """
        ***Note: Get data from single doc, which doesn't contain any `sub_collection`***\n
        :param collection_name: Example:`MongoDatabase.BOT_DATA`
        :param key: Key name to get value. e.g. `owner_id`
        :return str: Value of specified key | `None`
        """
        try:
            coll_data = self.database[collection_name]
            documents = coll_data.find_one()
            doc_value = documents.get(key)
            return doc_value
        except Exception as e:
            logger.error(e)


    def update(self, collection_name, search_key, match_value, data: dict):
        """
        :param collection_name: Example:`MongoDatabase.USERS_DATA`
        :param search_key: Key to search. e.g. `user_id`
        :param match_value: Value to match. e.g. `2134776547`
        :param data: dict Example: `{"name": "Bishal"}`
        :return bool: `True` | `False` | `None`
        """
        try:
            coll_data = self.database[collection_name]
            response = coll_data.update_one(
                {search_key: match_value},
                {"$set": data}
            )

            return response.acknowledged
        except Exception as e:
            logger.error(e)


    def info(self, collection_name=None):
        """
        :param collection_name: Example:`MongoDatabase.USERS_DATA`
        :return dict: Information about whole database or specified `collection` | `None`
        """
        try:
            doc_names = self.database.list_collection_names() if not collection_name else [collection_name]
            all_data = {}

            for coll_name in doc_names:
                doc_stats = self.database.command("collstats", coll_name)

                data = {
                    coll_name: {
                        "name": coll_name,
                        "quantity": doc_stats['count'],
                        "size": f"{doc_stats['storageSize'] / (1024 * 1024):.2f} MB",
                        "acsize": f"{doc_stats['size'] / (1024 * 1024):.2f} MB"
                    }
                }

                all_data.update(data)
            
            return all_data
        except Exception as e:
            logger.error(e)


    def delete_collection(self, collection_name):
        """
        ***Note: Task can't be undone.***\n
        :param collection_name: Name of the collection to delete. e.g. `bot_data`
        :return bool: `True` | `False` | `None`
        """
        try:
            coll_data = self.database[collection_name]
            response = coll_data.delete_many({})

            return response.acknowledged
        except Exception as e:
            logger.error(e)
    

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
