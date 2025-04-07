import os
import shutil
from telegram import Bot
from bot.config import load_config
from bot.logger import setup_logging

# constants
CONFIG_FILE = "config.env"
REQUIRED_DIRS = ["downloads", "temp", "sys"]
ORIGINAL_BOT_USERNAME = "MissCiri_bot"
ORIGINAL_BOT_ID = 6845693976
DEFAULT_ERROR_CHANNEL_ID = -1002675104487
HANDLERS_DIR = "bot/functions"

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

logger.info("""
Developed by
 ______     __     ______     __  __     ______     __        
/\  == \   /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \       
\ \  __<   \ \ \  \ \___  \  \ \  __ \  \ \  __ \  \ \ \____  
 \ \_____\  \ \_\  \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/ 
   
                            Library: python-telegram-bot
                            GitHub: https://github.com/bishalqx980
""")
