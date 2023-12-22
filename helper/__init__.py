import os
import logging
from telegram import Bot
from dotenv import load_dotenv
from helper.alive import alive

load_dotenv("config.env")

bot_token = os.getenv("bot_token")
server_url = os.getenv("server_url")
shortener_api_key = os.getenv("shortener_api_key")
mongodb_uri = os.getenv("mongodb_uri")
db_name = os.getenv("db_name")

bot = Bot(bot_token)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


print(
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
