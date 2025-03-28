from bot.modules.database import MemoryDB, MongoDB

def database_search(collection_name, search_key, match_value):
    """
    :param collection_name: Name of collection. e.g. `users`
    :param search_key: Key to search. e.g. `user_id`
    :param match_value: Value to match. e.g. `2134776547`
    :return: Speficied search data | `None`
    """
    if collection_name == "bot_data":
        find_db = MemoryDB.bot_data
    else:
        mem_coll_names = {
            "bot_data": "bot_data",
            "users": "user_data",
            "groups": "chat_data",
            "data_center": "data_center"
        }

        full_data = getattr(MemoryDB, mem_coll_names[collection_name])
        find_db = full_data.get(match_value)
        if not find_db:
            find_db = MongoDB.find_one(collection_name, search_key, match_value)
            if find_db:
                MemoryDB.insert(mem_coll_names[collection_name], match_value, find_db)
    
    if not find_db:
        return False, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!"
    else:
        return True, find_db


def database_add_user(user):
    user_data = MemoryDB.user_data.get(user.id)
    if user_data:
        return
    
    data = MongoDB.find_one("users", "user_id", user.id)
    if not data:
        data = {
            "user_id": user.id,
            "name": user.full_name,
            "username": user.username,
            "mention": user.mention_html(),
            "lang": user.language_code,
            "active_status": True
        }

        MongoDB.insert("users", data)
    # inserts data to memorydb
    MemoryDB.insert("user_data", user.id, data)
