from bot import ENV_CONFIG
from bot.modules.database import MemoryDB

def fetch_sudos():
    """retuns `list` of `sudo's` including **owner_id**"""
    sudo_users = MemoryDB.bot_data.get("sudo_users") or []
    sudo_users.append(int(ENV_CONFIG["owner_id"]))

    return sudo_users
