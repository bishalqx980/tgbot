from bot import ENV_CONFIG
from bot.modules.database import MemoryDB

async def _power_users():
    """
    retuns `list` of `sudo's` including **owner_id**
    """
    sudo_users = MemoryDB.bot_data.get("sudo_users")

    power_users = sudo_users if sudo_users else []
    power_users.append(int(ENV_CONFIG["owner_id"]))
    return power_users
