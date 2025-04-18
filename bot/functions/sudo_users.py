from bot import config
from bot.modules.database import MemoryDB

def fetch_sudos():
    """
    :returns list: list of sudo's including **owner_id**
    """
    owner_id = config.owner_id
    sudo_users = MemoryDB.bot_data.get("sudo_users") or []

    if owner_id not in sudo_users:
        sudo_users.append(owner_id)
    
    return sudo_users
