from bot import logger

class MemoryDatabase:
    def __init__(self):
        self.bot_data = {}
        self.users_data = {}
        self.chats_data = {}
        self.data_center = {}
    

    def insert(self, collection_name, identifier=None, data=None):
        """
        Available `collection_name`'s:\n
        (`bot_data`, `users_data`, `chats_data`, `data_center`)
        - `identifier`: key to find/store the data | example: chat.id `optional` "if not given, data will be inserted directly"
        - `data` type: dict
        """
        if not data:
            logger.error("MemoryDatabase: `data` parameter can't be None.")
            return
        
        collection = getattr(self, collection_name, None)
        if not collection_name:
            logger.error(f"MemoryDatabase: Invalid collection name: {collection}")
            return
        
        if identifier:
            load_data = collection.get(identifier)
            if load_data:
                load_data.update(data)
            else:
                collection[identifier] = data
        else:
            collection.update(data) # direct data insert
    

    def clear_all(self):
        """Clear all cached data (MemoryDB)"""
        self.bot_data.clear()
        self.users_data.clear()
        self.chats_data.clear()
        self.data_center.clear()
