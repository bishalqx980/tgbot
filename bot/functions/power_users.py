from bot import owner_id
from bot.modules.database.local_database import LOCAL_DATABASE

async def _power_users():
    """
    retuns `list` of `sudo's` including **owner_id**
    """
    bot_docs = await LOCAL_DATABASE.find("bot_docs")
    if bot_docs:
        sudo_users = bot_docs.get("sudo_users")

    power_users = sudo_users if sudo_users else []
    power_users.append(int(owner_id))
    return power_users
