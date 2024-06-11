import json
from bot import logger

STORAGE_PATH = "bot/misc/message_storage.json"

class MessageStorage:
    async def get_msg(collection, msg_key=None):
        """
        collection = db_collection_name eg. (callback_messages or other_msg)\n
        ! optional\n
        msg_key = which message you want from specified collection
        """
        try:
            with open(STORAGE_PATH, "r") as f:
                load_db = json.load(f)
            
            load_collection = load_db.get(collection)
            if msg_key:
                db_data = load_collection[msg_key]
                return db_data
            return load_collection
        except Exception as e:
            logger.error(e)
