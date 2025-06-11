import os
import shutil
from time import time
from telegram import Bot, __version__ as __ptbversion__
from .utils.config import CONFIG
from .utils.logger import setup_logging

# constants
__version__ = "1.4.2.518" # major.minor.patch.commits
CONFIG_FILE = "config.env"
REQUIRED_DIRS = ["downloads", "sys"]
ORIGINAL_BOT_USERNAME = "MissCiri_bot"
ORIGINAL_BOT_ID = 6845693976
DEFAULT_ERROR_CHANNEL_ID = -1002675104487
BOT_UPTIME = time()
PSNDL_DATABASE_URL = "https://psndl.pages.dev/database.json"
TL_LANG_CODES_URL = "https://telegra.ph/Language-Code-12-24"
TTS_LANG_CODES_URL = "https://telegra.ph/Text-to-speech---language-codes-tts-01-23"

# Creating Required Folder/Directories
try:
    for dir_name in REQUIRED_DIRS:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
except Exception as e:
    print(e)
    exit()

# logger & .env config file
logger = setup_logging() # need to execute after creating Required folders
config = CONFIG()
config.load_config(CONFIG_FILE)

if not config.validate():
    raise ValueError("Missing required configuration.")

# Main bot function
bot = Bot(config.bot_token)

logger.info(f"""
Developed by
 ______     __     ______     __  __     ______     __        
/\  == \   /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \       
\ \  __<   \ \ \  \ \___  \  \ \  __ \  \ \  __ \  \ \ \____  
 \ \_____\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/ 
   
    Version: {__version__}
    Library: python-telegram-bot {__ptbversion__}
    GitHub: https://github.com/bishalqx980
""")
