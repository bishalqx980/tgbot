import os
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive
from SafoneAPI import SafoneAPI
from g4f.client import Client as g4f

load_dotenv("config.env")

bot_token = os.getenv("bot_token")
owner_id = os.getenv("owner_id")
owner_username = os.getenv("owner_username")
bot_pic = os.getenv("bot_pic")
lang_code_list = os.getenv("lang_code_list")
welcome_img = os.getenv("welcome_img")
#optional
support_chat = os.getenv("support_chat")
telegraph = os.getenv("telegraph")
#database
mongodb_uri = os.getenv("mongodb_uri")
db_name = os.getenv("db_name")
#alive
server_url = os.getenv("server_url")
#api's
shortener_api_key = os.getenv("shortener_api_key")
omdb_api = os.getenv("omdb_api")
weather_api_key = os.getenv("weather_api_key")
render_api = os.getenv("render_api")
#safone api
safone_api = SafoneAPI()
chatgpt_limit = os.getenv("chatgpt_limit")
ai_imagine_limit = os.getenv("ai_imagine_limit")
usage_reset = os.getenv("usage_reset")
#g4f
g4f = g4f()

bot = Bot(bot_token)

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
