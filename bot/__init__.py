import os
import logging
from telegram import Bot
from dotenv import load_dotenv
from bot.alive import alive
from SafoneAPI import SafoneAPI

load_dotenv("config.env")

bot_token = os.getenv("BOT_TOKEN")
owner_id = os.getenv("OWNER_ID")
owner_username = os.getenv("OWNER_USERNAME")
bot_pic = os.getenv("BOT_PIC")
lang_code_list = os.getenv("LANG_CODE_LIST")
welcome_img = os.getenv("WELCOME_IMG")
#optional
support_chat = os.getenv("SUPPORT_CHAT")
telegraph = os.getenv("TELEGRAPH")
images = os.getenv("IMAGES")
#database
mongodb_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")
#alive
server_url = os.getenv("SERVER_URL")
#api's
shortener_api_key = os.getenv("SHORTENER_API_KEY")
omdb_api = os.getenv("OMDB_API")
weather_api_key = os.getenv("WEATHER_API_KEY")
render_api = os.getenv("RENDER_API")
#Limits
chatgpt_limit = os.getenv("CHATGPT_LIMIT")
ai_imagine_limit = os.getenv("AI_IMAGINE_LIMIT")
usage_reset = os.getenv("USAGE_RESET")

#safone api
safone_api = SafoneAPI()

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
