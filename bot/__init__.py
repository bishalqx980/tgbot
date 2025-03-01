import os
import time
import json
import shutil
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive

# Creating Required Folder/Directories
try:
    for dir_name in ["downloads", "temp", "sys"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
except Exception as e:
    print(e)
    exit(1)

# storing bot uptime on startup
open("sys/bot_uptime.txt", "w").write(str(time.time()))
# Creating log.txt file
open("sys/log.txt", "w")

#Enable logging
logging.basicConfig(
    filename="sys/log.txt", format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s", level=logging.INFO
)
#set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
# Disable Werkzeug logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)  # Use logging.CRITICAL to remove it completely

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)

config_file = load_dotenv("config.env")
if not config_file:
    logger.error("config.env not found...\nExiting...")
    exit(1)

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

#psndl
psndl_db = "https://raw.githubusercontent.com/bishalqx980/python/main/psndl%20(ps3)/psndl_db.json"

variables = [bot_token, mongodb_uri, db_name]
for variable in variables:
    if len(variable) == 0:
        logger.error(f"Check config.env again... [some value are empty]")
        exit(1)
    else:
        pass

# Local Database
LOCAL_DB = "sys/database.json"
localdb_default_structure = {"bot_docs": {}, "users": {}, "groups": {}, "data_center": {}}

check_local_db = os.path.isfile(LOCAL_DB)
if not check_local_db:
    logger.info("localdb not found...")
    json.dump({}, open(LOCAL_DB, "w"))
    logger.info("localdb created...")

try:
    json.dump(
        localdb_default_structure,
        open(LOCAL_DB, "w"),
        indent=4
    )
    logger.info("localdb updated...")
except Exception as e:
    logger.error(e)

# Main bot function
bot = Bot(bot_token)

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

# Server breathing
alive()
