from . import CONFIG_FILE, logger, config
from .modules.database import MemoryDB, MongoDB

def update_database():
    bot_data = MongoDB.find("bot_data", "_id")
    if bot_data:
        data = MongoDB.find_one("bot_data", "_id", bot_data[0])
        MemoryDB.insert("bot_data", None, data)
        logger.info("MongoDB database exist! Skiping update process!")
        return
    
    config_data = {
        "bot_token": config.bot_token,
        "owner_id": config.owner_id,
        "owner_username": config.owner_username,
        "show_bot_pic": config.show_bot_pic,
        "server_url": config.server_url,

        "mongodb_uri": config.mongodb_uri,
        "db_name": config.db_name,

        "shrinkme_api": config.shrinkme_api,
        "omdb_api": config.omdb_api,
        "weather_api": config.weather_api
    }
    
    try:
        MongoDB.insert("bot_data", config_data)
        MemoryDB.insert("bot_data", None, config_data)
        logger.info(f"Database has been updated from `{CONFIG_FILE}` file.")
    except Exception as e:
        logger.warning(e)
