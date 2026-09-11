import psutil
from time import time
from datetime import timedelta

from app import BOT_UPTIME


def _format_uptime(seconds: float) -> str:
    uptime = timedelta(seconds=seconds)

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m"


def system_uptime() -> dict:
    return {
        "system_uptime": _format_uptime(time() - psutil.boot_time()),
        "bot_uptime": _format_uptime(time() - BOT_UPTIME)
    }