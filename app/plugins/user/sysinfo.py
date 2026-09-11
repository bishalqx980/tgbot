import psutil
from time import time

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import privatechat_only
from app.database import MongoDB
from app.helpers import system_uptime
from app.modules.utils import UTILITY


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "sysinfo",
    "commands": ["sysinfo"], # list of commands including aliases

    "description": "Get system information.",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "System Info", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


class SysMenuData:
    DATA = {}

    TEXT = (
        "> **⌀ SystemInfo()**\n\n"

        "**❒ Uptime**\n"
        "**├ System uptime:** `{system_uptime}`\n"
        "**└ Bot uptime:** `{bot_uptime}`\n\n"

        "**❒ Server ({is_server_cached})**\n"
        "**├ Host:** `{server_ping}`\n"
        "**└ Telegram:** `{tg_server_ping}`\n\n"
        "<i>**Note:** Server cache value refreshes every 3 minute.</i>"
    )

    BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("CPU", "sysinfo:cpu"),
            InlineKeyboardButton("RAM", "sysinfo:ram")
        ],
        [
            InlineKeyboardButton("STORAGE", "sysinfo:storage"),
            InlineKeyboardButton("✘ Close", "sysinfo:close")
        ]
    ])


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
async def func_(_, message: Message):
    sent_message = await message.reply("Please wait...")

    # Getting system & bot uptime
    uptime = system_uptime()

    cache_time = SysMenuData.DATA.get("cache_time", 0)
    if (time() - cache_time) >= 3 * 60:
        # pinging server
        bot_data = MongoDB.get_bot_data()
        server_url = bot_data.get("server_url")
        
        server_ping = "~ infinite ~" # pre-determined
        if server_url:
            server_url = server_url if server_url.startswith("http") else f"http://{server_url}"
            server_ping = await UTILITY.pingServer(server_url)
        # Telegram Server Ping Check
        tg_server_ping = await UTILITY.pingServer("http://api.telegram.org/")

        # Updating Cache
        SysMenuData.DATA.update({
            "cache_time": time(),
            "server_ping": server_ping,
            "tg_server_ping": tg_server_ping
        })

        cache_value = False
    else:
        server_ping = SysMenuData.DATA.get("server_ping", "N/A")
        tg_server_ping = SysMenuData.DATA.get("tg_server_ping", "N/A")
        cache_value = True
    
    await sent_message.edit_text(
        SysMenuData.TEXT.format(
            system_uptime=uptime["system_uptime"],
            bot_uptime=uptime["bot_uptime"],
            is_server_cached="Cache" if cache_value else "Live",
            server_ping=server_ping,
            tg_server_ping=tg_server_ping
        ),
        reply_markup=SysMenuData.BUTTONS
    )


@bot.on_callback_query(filters.regex(r"sysinfo:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    # refined query data
    query_data = query.data.removeprefix("sysinfo:")
    # Default Variables
    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("☰ Menu", "sysinfo:menu"),
        InlineKeyboardButton("✘ Close", "sysinfo:close")
    ]])

    # Logics
    if query_data == "menu":
        # Getting system & bot uptime
        uptime = system_uptime()

        text = SysMenuData.TEXT.format(
            system_uptime=uptime["system_uptime"],
            bot_uptime=uptime["bot_uptime"],
            is_server_cached="Cache",
            server_ping=SysMenuData.DATA.get("server_ping", "N/A"), # already cached
            tg_server_ping=SysMenuData.DATA.get("tg_server_ping", "N/A") # already cached
        )

        btn = SysMenuData.BUTTONS
    
    elif query_data == "cpu":
        cpuUsagePercent = psutil.cpu_percent()
        cpuUsageBar = UTILITY.createProgressBar(cpuUsagePercent)

        text = (
            "> **⌀ SystemInfo()**\n\n"

            "**❒ CPU**\n"
            f"**├ CPU:** `{psutil.cpu_count()}`\n"
            f"**├ CPU (Logical):** `{psutil.cpu_count(False)}`\n"
            f"**├ CPU freq Current:** `{psutil.cpu_freq()[0]/1024:.2f} Ghz`\n"
            f"**├ CPU freq Max:** `{psutil.cpu_freq()[2]/1024:.2f} Ghz`\n"
            f"**└ CPU Usage Percent:** `{cpuUsagePercent} %`\n"
            f"**{cpuUsageBar}**\n\n"
        )
    
    elif query_data == "ram":
        ramPercent = psutil.virtual_memory()[2]
        swapRamPercent = psutil.swap_memory()[3]

        ramBar = UTILITY.createProgressBar(ramPercent)
        swapRamBar = UTILITY.createProgressBar(swapRamPercent)

        text = (
            "> **⌀ SystemInfo()**\n\n"

            "**❒ RAM**\n"
            f"**├ RAM Total:** `{psutil.virtual_memory()[0]/(1024**3):.2f} GB`\n"
            f"**├ RAM Avail:** `{psutil.virtual_memory()[1]/(1024**3):.2f} GB`\n"
            f"**├ RAM Used:** `{psutil.virtual_memory()[3]/(1024**3):.2f} GB`\n"
            f"**├ RAM Free:** `{psutil.virtual_memory()[4]/(1024**3):.2f} GB`\n"
            f"**└ RAM Percent:** `{ramPercent} %`\n"
            f"**{ramBar}**\n\n"

            "**❒ RAM (Swap)**\n"
            f"**├ RAM Total (Swap):** `{psutil.swap_memory()[0]/(1024**3):.2f} GB`\n"
            f"**├ RAM Used (Swap):** `{psutil.swap_memory()[1]/(1024**3):.2f} GB`\n"
            f"**├ RAM Free (Swap):** `{psutil.swap_memory()[2]/(1024**3):.2f} GB`\n"
            f"**└ RAM Percent (Swap):** `{swapRamPercent} %`\n"
            f"**{swapRamBar}**\n\n"
        )

    elif query_data == "storage":
        diskUsagePercent = psutil.disk_usage("/")[3]
        diskUsageBar = UTILITY.createProgressBar(diskUsagePercent)

        text = (
            "> **⌀ SystemInfo()**\n\n"

            "**❒ Storage**\n"
            f"**├ Total Partitions:** `{len(psutil.disk_partitions())}`\n"
            f"**├ Disk Usage Total:** `{psutil.disk_usage('/')[0]/(1024**3):.2f} GB`\n"
            f"**├ Disk Usage Used:** `{psutil.disk_usage('/')[1]/(1024**3):.2f} GB`\n"
            f"**├ Disk Usage Free:** `{psutil.disk_usage('/')[2]/(1024**3):.2f} GB`\n"
            f"**└ Disk Usage Percent:** `{diskUsagePercent} %`\n"
            f"**{diskUsageBar}**\n\n"
        )
    
    elif query_data == "close":
        try:
            await query.answer()
        except: pass
        try:
            message_id = query.message.id
            await bot.delete_messages(query.message.chat.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except: pass
        return
    
    # global reply
    try:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
