from bot.modules.database import MemoryDB, MongoDB

def database_search(collection_name, search_key, match_value):
    """
    :param collection_name: Name of collection. e.g. `users`
    :param search_key: Key to search. e.g. `user_id`
    :param match_value: Value to match. e.g. `2134776547`
    :return: Speficied search data | `Error: Chat isn't registered.`
    """
    data = None

    if collection_name == "bot_data":
        data = MemoryDB.bot_data
    
    else:
        mem_coll_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }
        
        # getting all data of `collection_name` that stored in Memory
        memory_data = getattr(MemoryDB, mem_coll_names[collection_name])
        # matched data
        data = memory_data.get(match_value)

        if not data:
            data = MongoDB.find_one(collection_name, search_key, match_value)
            if data:
                MemoryDB.insert(mem_coll_names[collection_name], match_value, data)
    
    return data


def database_add_user(user):
    """
    ***Checks Memory for `user_data` if not found then checks on MongoDB & updates `user_data` to Memory & MongoDB***\n
    :param user: `update.effective_user`
    """
    user_data = MemoryDB.user_data.get(user.id)
    if user_data:
        return
    
    user_data = MongoDB.find_one("users", "user_id", user.id)
    if not user_data:
        user_data = {
            "user_id": user.id,
            "name": user.full_name,
            "username": user.username,
            "mention": user.mention_html(),
            "lang": user.language_code,
            "active_status": True
        }

        MongoDB.insert("users", user_data)
    # inserts data to memorydb
    MemoryDB.insert("user_data", user.id, user_data)
