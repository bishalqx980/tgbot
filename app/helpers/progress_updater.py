from time import time
from datetime import timedelta

from pyrogram.types import Message

from app import logger
from app.modules.utils import UTILITY


async def tgProgressUpdater(current, total, message: Message, statusMessage: str = "", startTime = None):
    """
    ***Note: current & total param are default required param for pyrogram downloader (leave these)***

    :param message: Editable sent message (not caption)
    :param statusMessage: info text (E.g. "Downloading" or "Uploading")
    :param startTime: Progress start timestamp (time.time()) / otherwise it will not show correct ETA
    """
    try:
        if startTime is None:
            startTime = time() # everything reset? it has bug maybe
        
        percent = current * 100 / total
        elapsedTime = time() - startTime
        elapsed = timedelta(seconds=int(elapsedTime))

        # Speed in MB/s (bytes -> MB)
        currentSpeed = current / elapsedTime / (1024 * 1024)

        # Remaining time
        remainingSeconds = (total - current) / (currentSpeed * 1024 * 1024)
        remaining = timedelta(seconds=int(remainingSeconds))

        await message.edit_text(
            f"**{statusMessage}**\n"
            f"**Speed:** `{currentSpeed:.2f}MB/s`\n"
            f"**Elapsed:** `{elapsed}`\n"
            f"**ETA:** `{remaining}`\n"
            f"**Progress:** `{UTILITY.createProgressBar(int(percent))} {percent:.2f}%`"
        )
    except Exception as e:
        logger.error(e)
