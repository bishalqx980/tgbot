from bot.modules.mongodb import MongoDB
from bot.modules.local_database import LOCAL_DATABASE
from bot import (
    logger,
    bot_token,
    owner_id,
    owner_username,
    bot_pic,
    welcome_img,
    github_repo,
    mongodb_uri,
    db_name,
    server_url,
    shrinkme_api,
    omdb_api,
    weather_api
)


async def update_database():
    find = await MongoDB.find("bot_docs", "_id")

    if find:
        logger.info("MongoDB database exist! Skiping update...")
        return
    
    data = {
        "bot_token": bot_token,
        "owner_id": int(owner_id),
        "owner_username": owner_username,
        "bot_pic": bot_pic,
        "welcome_img": bool(welcome_img),
        "github_repo": github_repo,
        #database
        "mongodb_uri": mongodb_uri,
        "db_name": db_name,
        #alive
        "server_url": server_url,
        #api's
        "shrinkme_api": shrinkme_api,
        "omdb_api": omdb_api,
        "weather_api": weather_api
    }

    try:
        await MongoDB.insert_single_data("bot_docs", data)
        await LOCAL_DATABASE.insert_data_direct("bot_docs", data)
        logger.info("Database updated from config.env ...")
        return True
    except Exception as e:
        logger.warning(e)
        return False
