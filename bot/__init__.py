import os
import shutil
from time import time
from telegram import Bot
from .config import load_config
from .logger import setup_logging

# constants
__version__ = "1.0.4.486" # major.minor.patch.commits
CONFIG_FILE = "config.env"
REQUIRED_DIRS = ["downloads", "sys"]
ORIGINAL_BOT_USERNAME = "MissCiri_bot"
ORIGINAL_BOT_ID = 6845693976
DEFAULT_ERROR_CHANNEL_ID = -1002675104487
HANDLERS_DIR = "bot/functions"
BOT_UPTIME = time()
BOT_HANDLERS_COUNT = {}

# Creating Required Folder/Directories
try:
    for dir_name in REQUIRED_DIRS:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
except Exception as e:
    print(e)
    exit()

# logger & env config file
logger = setup_logging() # need to execute after creating Required folders
ENV_CONFIG = load_config(CONFIG_FILE)

# Main bot function
bot = Bot(ENV_CONFIG["bot_token"])

logger.info(f"""
Developed by
 ______     __     ______     __  __     ______     __        
/\  == \   /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \       
\ \  __<   \ \ \  \ \___  \  \ \  __ \  \ \  __ \  \ \ \____  
 \ \_____\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/ 
   
    Version: {__version__}
    Library: python-telegram-bot
    GitHub: https://github.com/bishalqx980
""")
