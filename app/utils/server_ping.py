import asyncio
import aiohttp

from app import logger, RUN_SERVER
from app.database import MongoDB
from app.utils.server.server import RunServer


async def keep_server_alive():
    if not RUN_SERVER:
        return

    RunServer()
    
    bot_data = MongoDB.get_bot_data()
    server_url = bot_data.get("server_url")
    sleeptime = 180 # 3 min

    if not server_url:
        logger.warning(
            "Server URL wasn't found...!"
        )
        return
    
    while True:

        # Everytime check if there is new server_url
        bot_data = MongoDB.get_bot_data()
        server_url = bot_data.get("server_url")

        if not server_url:
            await asyncio.sleep(sleeptime)
            return
        
        if not server_url.startswith("http"):
            server_url = f"http://{server_url}"
        
        try:

            async with aiohttp.ClientSession() as session:
                async with session.get(server_url) as response:
                    if not response.ok:
                        logger.warning(
                            f"{response.status} - {server_url} is down or unreachable."
                        )

        except Exception as e:
            logger.error(e)
        
        await asyncio.sleep(sleeptime)
