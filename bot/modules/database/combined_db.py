from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def global_search(collection, search, match):
    """
    collection: collection_name\n
    search: eg user_id, chat_id\n
    match: eg. user.id, chat.id\n
    workflow > search on local_db > if not found > search on mongodb > return bool or find_user/find_group = [1]
    """
    if collection == "bot_docs":
        find_db = await LOCAL_DATABASE.find(collection)
        if not find_db:
            find = await MongoDB.find("bot_docs", "_id")
            find_db = await MongoDB.find_one("bot_docs", "_id", find[0])
    else:
        find_db = await LOCAL_DATABASE.find_one(collection, match)
        if not find_db:
            find_db = await MongoDB.find_one(collection, search, match)
            if find_db:
                await LOCAL_DATABASE.insert_data(collection, match, find_db)
    
    if not find_db:
        return False, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!"
    else:
        return True, find_db


async def find_bot_docs():
    """
    workflow > search on local_db > if not found > search on mongodb > return error or _bot
    """
    _bot = await LOCAL_DATABASE.find("bot_docs")
    if not _bot:
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        if not _bot:
            logger.error("_bot not found in mongodb...")
            return
        await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)
    return _bot


async def check_add_user_db(user):
    """
    workflow > check local_db for user, if not > check mongodb if not > add data else nothing
    """
    find_user = await LOCAL_DATABASE.find_one("users", user.id)
    if not find_user:
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if find_user:
            await LOCAL_DATABASE.insert_data("users", user.id, find_user)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True
            }

            await MongoDB.insert_single_data("users", data)
            await LOCAL_DATABASE.insert_data("users", user.id, data)
