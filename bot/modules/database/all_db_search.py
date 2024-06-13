from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def all_db_search(collection, search, match):
    """
    collection: collection_name\n
    search: eg user_id, chat_id\n
    match: eg. user.id, chat.id\n
    uses > find_one
    """
    find_db = await LOCAL_DATABASE.find_one(collection, match)
    if not find_db:
        find_db = await MongoDB.find_one(collection, search, match)
        if find_db:
            data = find_db
            await LOCAL_DATABASE.insert_data(collection, match, data)
    
    if not find_db:
        return False, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!"
    else:
        return True, find_db
