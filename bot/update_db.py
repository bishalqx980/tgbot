from bot.modules.mongodb import MongoDB
from bot import (
    logger,
    bot_token,
    owner_id,
    owner_username,
    bot_pic,
    lang_code_list,
    welcome_img,
    support_chat,
    telegraph,
    images,
    mongodb_uri,
    db_name,
    server_url,
    shortener_api_key,
    omdb_api,
    weather_api_key,
    render_api,
    safone_api,
    chatgpt_limit,
    ai_imagine_limit,
    usage_reset
)


async def update_database():
    find = await MongoDB.find("bot_docs", "_id")

    if find:
        logger.info("MongoDB Database Exist! Skiping update...")
        return
    
    data = {
        "bot_token": bot_token,
        "owner_id": int(owner_id),
        "owner_username": owner_username,
        "bot_pic": bot_pic,
        "lang_code_list": lang_code_list,
        "welcome_img": bool(welcome_img),
        #optional
        "support_chat": support_chat,
        "telegraph": telegraph,
        "images": images,
        #database
        "mongodb_uri": mongodb_uri,
        "db_name": db_name,
        #alive
        "server_url": server_url,
        #api's
        "shortener_api_key": shortener_api_key,
        "omdb_api": omdb_api,
        "weather_api_key": weather_api_key,
        "render_api": render_api,
        #limits
        "chatgpt_limit": int(chatgpt_limit),
        "ai_imagine_limit": int(ai_imagine_limit),
        "usage_reset": int(usage_reset)
    }

    try:
        await MongoDB.insert_single_data("bot_docs", data)
        logger.info("Database updated from config.env ...")
        return True
    except Exception as e:
        logger.warning(f"Error: {e}")
        return False
