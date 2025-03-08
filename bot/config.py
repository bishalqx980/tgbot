import os
from dotenv import load_dotenv

def load_config(config_file):
    """
    `config_file`: .env file path\n
    returns variables `dict`
    """
    # loading config file
    load_dotenv(config_file)
    # variables dict
    return {
        "bot_token": os.getenv("BOT_TOKEN"),
        "owner_id": os.getenv("OWNER_ID"),
        "owner_username": os.getenv("OWNER_USERNAME"),
        "bot_pic": os.getenv("BOT_PIC"),
        #database
        "mongodb_uri": os.getenv("MONGODB_URI"),
        "db_name": os.getenv("DB_NAME"),
        #alive
        "server_url": os.getenv("SERVER_URL"),
        #api's
        "shrinkme_api": os.getenv("SHRINKME_API"),
        "omdb_api": os.getenv("OMDB_API"),
        "weather_api": os.getenv("WEATHER_API")
    }
