import re
from time import time
from discord_webhook import DiscordWebhook

from bot import logger
from bot.utils.database import MemoryDB


def send_discord_message(message):
    """
    :param message: The message you want to send to discord (supports markdown)
    """
    discord_webhook = MemoryDB.bot_data.get("discord_webhook")
    if not discord_webhook:
        logger.error("discord_webhook not found!")
        return
    
    try:
        # Removing HTML tags
        message = re.sub(r"<.*?>", "", message)
        # Sending message
        webhook = DiscordWebhook(
            url=discord_webhook,
            content=(
                f"{message}\n"
                f"> **Received: <t:{int(time())}:R>** - || <@&1462103653883314287> ||" # Tag Me role
            )
        )
        webhook.execute()
    except Exception as e:
        logger.error(e)
