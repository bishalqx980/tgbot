import os
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive
from SafoneAPI import SafoneAPI

load_dotenv("config.env")

bot_token = os.getenv("bot_token")
owner_id = os.getenv("owner_id")
owner_username = os.getenv("owner_username")
# database
mongodb_uri = os.getenv("mongodb_uri")
db_name = os.getenv("db_name")
# alive
server_url = os.getenv("server_url")
# api's
shortener_api_key = os.getenv("shortener_api_key")
omdb_api = os.getenv("omdb_api")
# safone api
safone_api = SafoneAPI()
chatgpt_usage_limit = os.getenv("chatgpt_usage_limit")
chatgpt_usage_reset_time = os.getenv("chatgpt_usage_reset_time")

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
