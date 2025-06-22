from .memory_database import MemoryDatabase
from .mongodb import MongoDatabase

# Database Constants
class DBConstants:
    BOT_DATA = "bot_data"
    USERS_DATA = "users_data"
    CHATS_DATA = "chats_data"
    # only for MemoryDB
    DATA_CENTER = "data_center"

# initializing
MemoryDB = MemoryDatabase()
MongoDB = MongoDatabase()

# Helper functions
def database_search(collection_name, search_key, match_value):
    """
    :param collection_name: Name of collection. e.g. `users_data`
    :param search_key: Key to search. e.g. `user_id`
    :param match_value: Value to match. e.g. `2134776547`
    :return: Speficied search data | `Error: None; Which means chat isn't registered.`
    """
    data = None

    if collection_name == DBConstants.BOT_DATA:
        data = MemoryDB.bot_data
    
    else:
        # getting all data of `collection_name` that stored in Memory
        memory_data = getattr(MemoryDB, collection_name)
        # matched data
        data = memory_data.get(match_value)

        if not data:
            data = MongoDB.find_one(collection_name, search_key, match_value)
            if data:
                MemoryDB.insert(collection_name, match_value, data)
    
    return data


def database_add_user(user):
    """
    ***Checks Memory for `users_data` if not found then checks on MongoDB & updates `users_data` to Memory & MongoDB***\n
    :param user: `update.effective_user`
    """
    user_data = MemoryDB.users_data.get(user.id)
    if user_data:
        return
    
    user_data = MongoDB.find_one(DBConstants.USERS_DATA, "user_id", user.id)
    if not user_data:
        user_data = {
            "user_id": user.id,
            "name": user.full_name,
            "username": user.username,
            "lang": user.language_code,
            "active_status": True
        }

        MongoDB.insert(DBConstants.USERS_DATA, user_data)
    # inserts data to memorydb
    MemoryDB.insert(DBConstants.USERS_DATA, user.id, user_data)
