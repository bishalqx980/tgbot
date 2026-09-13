import os
import json
import shutil
from time import time
from pathlib import Path

from pyrogram import Client, __version__ as __pyroVersion__
from pyrogram.types import LinkPreviewOptions
from pyrogram.enums import ClientPlatform

from app.utils.logger import setup_logging
from config import CONFIG

# Version Tracker
version_tracker = json.load(open("version.json", "rb"))
__version__ = version_tracker["__version__"] # major.minor.patch.commits
__versionStatus__ = version_tracker["__status__"] # Stable / Beta
__githubVersionURL__ = "https://raw.githubusercontent.com/bishalqx980/tgbot/refs/heads/v2/version.json"

# constants
MODULES = {}
FAILED_TO_LOAD_MODULES = [] # contains error message str
HELP_MENU_CATEGORIES = ["user", "group", "ai", "admin"]
ADMIN_CATEGORIES = ["admin"]
PLUGINS_PATH = Path("app/plugins") # Path("path")

BOT_UPTIME = time()
BOT_SETTINGS_EXTRA_CONFIG = [
    "sudo_users",
    
    "omdb_api",
    "shrinkme_api",
    "forecast_api",

    "bool_botpic",
    "bot_images",
    "link_supportchat",
    "server_url",
]
ORIGINAL_BOT_USERNAME = "MissCiri_bot" # without @
ORIGINAL_BOT_ID = 6845693976
SERVER_LOG_CHANNEL_ID = -1002675104487
COMMAND_PREFIXES = ["/", "-", "!", "."]
REQUIRED_DIRS = ["downloads", "sys"]
WORK_DIR = Path("sys")
RUN_SERVER = True # switch to run flask server
# Links
PSNDL_WEBSITE_URL = "https://bishalqx980.github.io/psndl/"
PSNDL_DATABASE_URL = "https://psndl.pages.dev/database.json"
TL_LANG_CODES_URL = "https://telegra.ph/Language-Code-12-24"
TTS_LANG_CODES_URL = "https://telegra.ph/Text-to-speech---language-codes-tts-01-23"


# Creating Required Folders/Directories
try:
    for dir_name in REQUIRED_DIRS:
        if os.path.exists(dir_name):
            if dir_name != "sys": # Exception for sys dir (to keep client cache file on restart)
                shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
except Exception as e:
    print(e)
    exit()

# logger & config
logger = setup_logging()
config = CONFIG()

# Main Client function
bot = Client(
    name=ORIGINAL_BOT_USERNAME,
    api_id=config.api_id,
    api_hash=config.api_hash,
    app_version=f"{__pyroVersion__} x64",
    device_model="Desktop",
    system_version="Windows 11 x64",
    bot_token=config.bot_token,
    workdir=WORK_DIR,
    client_platform=ClientPlatform.DESKTOP,
    link_preview_options=LinkPreviewOptions(is_disabled=True)
)

logger.info(f"""
# 𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓭 𝓫𝔂

#  ▄▄▄▄    ██▓  ██████  ██░ ██  ▄▄▄       ██▓    
# ▓█████▄ ▓██▒▒██    ▒ ▓██░ ██▒▒████▄    ▓██▒    
# ▒██▒ ▄██▒██▒░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ▒██░    
# ▒██░█▀  ░██░  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ▒██░    
# ░▓█  ▀█▓░██░▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░██████▒
# ░▒▓███▀▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░
# ▒░▒   ░  ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░
#  ░    ░  ▒ ░░  ░  ░   ░  ░░ ░  ░   ▒     ░ ░   
#  ░       ░        ░   ░  ░  ░      ░  ░    ░  ░
#       ░                                        

#     Version ({__versionStatus__}): {__version__}
#     Library: kurigram {__pyroVersion__}
#     GitHub: https://github.com/bishalqx980
""")
