import os
import json
import shutil
from time import time
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive
from bot.logger import setup_logging

# Creating Required Folder/Directories
try:
    for dir_name in ["downloads", "temp", "sys"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
except Exception as e:
    print(e)
    exit()

# constants
CONFIG_FILE = "config.env"
LOCAL_DB = "sys/database.json"
LOCAL_DB_DEFAULT = {"bot_docs": {}, "users": {}, "groups": {}, "data_center": {}}

# logger
logger = setup_logging()

# storing bot uptime on startup
open("sys/bot_uptime.txt", "w").write(str(time()))

# loading config file
if not load_dotenv(CONFIG_FILE):
    logger.error("config.env not found...\nExiting...")
    exit()

bot_token = os.getenv("BOT_TOKEN")
owner_id = os.getenv("OWNER_ID")
owner_username = os.getenv("OWNER_USERNAME")
bot_pic = os.getenv("BOT_PIC")
welcome_img = os.getenv("WELCOME_IMG")
#database
mongodb_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")
#alive
server_url = os.getenv("SERVER_URL")
#api's
shrinkme_api = os.getenv("SHRINKME_API")
omdb_api = os.getenv("OMDB_API")
weather_api = os.getenv("WEATHER_API")

variables = [bot_token, mongodb_uri, db_name]
for variable in variables:
    if len(variable) == 0:
        logger.error(f"Check config.env again... (some values are empty)")
        exit()
    else:
        pass

# Local Database
check_local_db = os.path.isfile(LOCAL_DB)
if not check_local_db:
    logger.info("localdb not found...")
    json.dump({}, open(LOCAL_DB, "w"))
    logger.info("localdb created...")

try:
    json.dump(
        LOCAL_DB_DEFAULT,
        open(LOCAL_DB, "w"),
        indent=4
    )
    logger.info("localdb updated...")
except Exception as e:
    logger.error(e)

# Main bot function
bot = Bot(bot_token)

# Server breathing
alive()

logger.info(
'''
Developed by

 ▄▄▄▄    ██▓  ██████  ██░ ██  ▄▄▄       ██▓    
▓█████▄ ▓██▒▒██    ▒ ▓██░ ██▒▒████▄    ▓██▒    
▒██▒ ▄██▒██▒░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ▒██░    
▒██░█▀  ░██░  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ▒██░    
░▓█  ▀█▓░██░▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░██████▒
░▒▓███▀▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░
▒░▒   ░  ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░
 ░    ░  ▒ ░░  ░  ░   ░  ░░ ░  ░   ▒     ░ ░   
 ░       ░        ░   ░  ░  ░      ░  ░    ░  ░
      ░                                        
                            Library python-telegram-bot
'''
)
