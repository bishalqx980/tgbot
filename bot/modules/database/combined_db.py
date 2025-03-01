from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def global_search(collection_name, search, match):
    """
    `collection_name` example `users` | `search` example `user_id` | `match` example `2134776547`\n
    returns `data` | `None`

    -- search flow --\n
    search on local database\n
        if not found > search on MongoDB\n
    returns `boolean`, `data`/`error message`
    """
    if collection_name == "bot_docs":
        find_db = await LOCAL_DATABASE.find(collection_name)
        if not find_db:
            find = await MongoDB.find("bot_docs", "_id")
            find_db = await MongoDB.find_one("bot_docs", "_id", find[0])
    else:
        find_db = await LOCAL_DATABASE.find_one(collection_name, match)
        if not find_db:
            find_db = await MongoDB.find_one(collection_name, search, match)
            if find_db:
                await LOCAL_DATABASE.insert_data(collection_name, match, find_db)
    
    if not find_db:
        return False, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!"
    else:
        return True, find_db


async def find_bot_docs():
    """
    -- search flow --\n
    search on local database\n
        if not found > search on MongoDB\n
    returns `bot_docs` | `None`
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
    Check & Add user in database\n
    -- search flow --\n
    search on local database\n
        if not found > search on MongoDB\n
    """
    find_user = await LOCAL_DATABASE.find_one("users", user.id)
    if find_user:
        return
    
    data = await MongoDB.find_one("users", "user_id", user.id)
    if not data:
        data = {
            "user_id": user.id,
            "name": user.full_name,
            "username": user.username,
            "mention": user.mention_html(),
            "lang": user.language_code,
            "active_status": True
        }

        await MongoDB.insert_single_data("users", data)
    # inserts data to localdb
    await LOCAL_DATABASE.insert_data("users", user.id, data)
