import os
import json
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive

with open('log.txt', 'w'):
    pass

#Enable logging
logging.basicConfig(
    filename="log.txt", format="%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s", level=logging.INFO
)
#set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s")
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
github_repo = os.getenv("GITHUB_REPO")
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
        logger.error(f"Check config.env again... [some value are empty]")
        exit(1)
    else:
        pass

LOCAL_DB = "database.json"

check_local_db = os.path.isfile(LOCAL_DB)
if not check_local_db:
    logger.info("localdb not found...")
    with open(LOCAL_DB, "w") as f:
        json.dump({}, f)
    logger.info("localdb created...")

try:
    with open(LOCAL_DB, "w") as f:
        data = {"bot_docs": {}, "users": {}, "groups": {}, "data_center": {}}
        json.dump(data, f, indent=4)
        logger.info("localdb updated...")
except Exception as e:
    logger.error(e)

bot = Bot(bot_token)

logger.info(
'''Developed by
__________.__       .__           .__   
\______   \__| _____|  |__ _____  |  |  
 |    |  _/  |/  ___/  |  \ \__ \ |  |  
 |    |   \  |\___ \|   Y  \/ __ \|  |__
 |______  /__/____  >___|  (____  /____/
        \/        \/     \/     \/      
                        Library python-telegram-bot'''
)

alive()
