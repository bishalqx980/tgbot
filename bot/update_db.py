from bot import CONFIG_FILE, logger
from bot.config import load_config
from bot.modules.database import MemoryDB, MongoDB

def update_database():
    env_config = load_config(CONFIG_FILE)

    bot_data = MongoDB.find("bot_data", "_id")
    if bot_data:
        data = MongoDB.find_one("bot_data", "_id", bot_data[0])
        MemoryDB.insert_data("bot_data", None, data)
        logger.info("MongoDB database exist! Skiping update process!")
        return
    
    try:
        MongoDB.insert_single_data("bot_data", env_config)
        MemoryDB.insert_data("bot_data", None, env_config)
        logger.info(f"Database has been updated from `{CONFIG_FILE}` file.")
    except Exception as e:
        logger.warning(e)
