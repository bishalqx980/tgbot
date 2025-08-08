import psutil
import aiohttp
from time import time
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from bot import BOT_UPTIME
from bot.utils.database import MemoryDB
from bot.modules.utils import Utils
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sent_message = await update.effective_message.reply_text("⌛")
    
    # Uptime Calculating
    sys_uptime = timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())

    sys_days = sys_uptime.days
    sys_hours, remainder = divmod(sys_uptime.seconds, 3600)
    sys_minute = remainder / 60

    bot_uptime = timedelta(seconds=time() - BOT_UPTIME)
    
    bot_days = bot_uptime.days
    bot_hours, remainder = divmod(bot_uptime.seconds, 3600)
    bot_minute = remainder / 60

    # System info variables
    ramPercent = psutil.virtual_memory()[2]
    swapRamPercent = psutil.swap_memory()[3]
    diskUsagePercent = psutil.disk_usage('/')[3]

    # percent vizualize
    ramBar = Utils.createProgressBar(ramPercent)
    swapRamBar = Utils.createProgressBar(swapRamPercent)
    diskUsageBar = Utils.createProgressBar(diskUsagePercent)

    # pinging server
    server_url = MemoryDB.bot_data.get("server_url")
    server_ping = "~ infinite ~" # pre-determined
    if server_url:
        if not server_url.startswith("http"):
            server_url = f"http://{server_url}"
        
        server_ping = await Utils.pingServer(server_url)
    # Telegram Server Ping Check
    tg_server_ping = await Utils.pingServer("http://api.telegram.org/")
    
    sys_info = (
        "<blockquote><b>🖥️ System information</b></blockquote>\n\n"

        "<b>🔹 CPU</b>\n"
        f"<b>├ CPU:</b> <code>{psutil.cpu_count()}</code>\n"
        f"<b>├ CPU (Logical):</b> <code>{psutil.cpu_count(False)}</code>\n"
        f"<b>├ CPU freq Current:</b> <code>{psutil.cpu_freq()[0]/1024:.2f} Ghz</code>\n"
        f"<b>└ CPU freq Max:</b> <code>{psutil.cpu_freq()[2]/1024:.2f} Ghz</code>\n\n"

        "<b>🔸 RAM</b>\n"
        f"<b>├ RAM Total:</b> <code>{psutil.virtual_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"<b>├ RAM Avail:</b> <code>{psutil.virtual_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"<b>├ RAM Used:</b> <code>{psutil.virtual_memory()[3]/(1024**3):.2f} GB</code>\n"
        f"<b>├ RAM Free:</b> <code>{psutil.virtual_memory()[4]/(1024**3):.2f} GB</code>\n"
        f"<b>└ RAM Percent:</b> <code>{ramPercent} %</code>\n"
        f"<b>{ramBar}</b>\n\n"

        "<b>🔸 RAM (Swap)</b>\n"
        f"<b>├ RAM Total (Swap):</b> <code>{psutil.swap_memory()[0]/(1024**3):.2f} GB</code>\n"
        f"<b>├ RAM Used (Swap):</b> <code>{psutil.swap_memory()[1]/(1024**3):.2f} GB</code>\n"
        f"<b>├ RAM Free (Swap):</b> <code>{psutil.swap_memory()[2]/(1024**3):.2f} GB</code>\n"
        f"<b>└ RAM Percent (Swap):</b> <code>{swapRamPercent} %</code>\n"
        f"<b>{swapRamBar}</b>\n\n"

        "<b>📦 Storage</b>\n"
        f"<b>├ Total Partitions:</b> <code>{len(psutil.disk_partitions())}</code>\n"
        f"<b>├ Disk Usage Total:</b> <code>{psutil.disk_usage('/')[0]/(1024**3):.2f} GB</code>\n"
        f"<b>├ Disk Usage Used:</b> <code>{psutil.disk_usage('/')[1]/(1024**3):.2f} GB</code>\n"
        f"<b>├ Disk Usage Free:</b> <code>{psutil.disk_usage('/')[2]/(1024**3):.2f} GB</code>\n"
        f"<b>└ Disk Usage Percent:</b> <code>{diskUsagePercent} %</code>\n"
        f"<b>{diskUsageBar}</b>\n\n"

        "<b>⚜️ Uptime</b>\n"
        f"<b>├ System uptime:</b> <code>{int(sys_days)}d {int(sys_hours)}h {int(sys_minute)}m</code>\n"
        f"<b>└ Bot uptime:</b> <code>{int(bot_days)}d {int(bot_hours)}h {int(bot_minute)}m</code>\n\n"

        "<b>🌐 Server</b>\n"
        f"<b>└ Ping:</b> <code>{server_ping}</code>\n"
        f"<b>└ Telegram:</b> <code>{tg_server_ping}</code>"
    )

    await sent_message.edit_text(sys_info)
