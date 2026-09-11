import aiohttp
from time import time

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "ping",
    "commands": ["ping"], # list of commands including aliases

    "description": "Ping any url / site. E.g. `/ping http://google.com`",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Ping", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    url = CommandArgs(message.text, message.command)

    if not url:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_message = await message.reply(f"Pinging {url}\nPlease wait...")

    try:
        async with aiohttp.ClientSession() as session:
            # Response time counting starts
            start_time = time()
            # Sending req
            async with session.get(url, timeout=aiohttp.ClientTimeout(10)) as response:
                response_time = int((time() - start_time) * 1000) # converting to ms
                if response_time > 1000:
                    response_time = f"{(response_time / 1000):.2f}s"
                else:
                    response_time = f"{response_time}ms"
                
                status_codes = {
                    200: "✅ Online",
                    201: "✅ Created",
                    202: "✅ Accepted",
                    204: "⚠️ No Content",
                    301: "➡️ Moved Permanently",
                    302: "➡️ Found (Redirect)",
                    400: "❌ Bad Request",
                    401: "🔒 Unauthorized",
                    403: "🚫 Forbidden",
                    404: "❌ Not Found",
                    408: "⏳ Request Timeout",
                    500: "🔥 Internal Server Error",
                    502: "⚠️ Bad Gateway",
                    503: "⚠️ Service Unavailable"
                }

                status = status_codes.get(response.status, "⚠️ Unknown Status")
                text = (
                    f"Site: {url}\n"
                    f"R.time: `{response_time}`\n"
                    f"R.code: `{response.status}`\n"
                    f"Status: `{status}`"
                )
    except aiohttp.ServerTimeoutError:
        text = "Error: Request timeout."
    except aiohttp.ServerConnectionError:
        text = "Error: Connection error."
    except Exception as e:
        text = f"Error: {e or 'An unknown error occurred.'}"
    
    await sent_message.edit_text(f"**{text}**")
