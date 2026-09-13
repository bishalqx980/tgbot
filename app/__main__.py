import asyncio
import requests

from pyrogram import idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeAllPrivateChats

from app import bot, logger, config, __version__, __versionStatus__, __githubVersionURL__, MODULES, FAILED_TO_LOAD_MODULES
from app.modules import telegraph
from app.utils.loader import load_plugins
from app.utils.update_database import update_database
from app.utils.server_ping import keep_server_alive


async def app_init():
    # Update Database info/config
    update_database_res = update_database()
    # Initialize Telegraph
    telegraph_res = await telegraph.initialize()

    try:
        await bot.delete_bot_commands()
        botcmdres = await bot.set_bot_commands([
            BotCommand("start", "Bot intro!"),
            BotCommand("help", "Get help!"),
            BotCommand("support", "Contact with bot's support team!"),
        ], BotCommandScopeAllPrivateChats())
    except Exception as e:
        logger.error(e)
        botcmdres = None

    try:

        try:

            is_latest = "???"

            res = requests.get(__githubVersionURL__)
            if res.ok:
                data = res.json()
                __githubVersion__ = data.get("__version__")

            if __version__ == __githubVersion__:
                is_latest = "latest"

            else:
                is_latest = "outdated"

        except Exception as e:
            logger.error(e)
        
        await bot.send_message(
            config.owner_id,
            (
                "> **App Started!**\n\n"

                f"**$modules loaded : <i>{len(MODULES)}</i>**\n"
                f"**$failed to loaded : <i>{len(FAILED_TO_LOAD_MODULES)}</i>**\n"
                f"**$database : <i>{update_database_res}</i>**\n"
                f"**$telegraph : <i>{telegraph_res}</i>**\n"
                f"**$botcommand : <i>{'Updated!' if botcmdres else 'Failed to update!'}</i>**\n\n"

                f"> **Version (<i>{__versionStatus__}</i>)** : **{__version__}** ({is_latest})"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Start", url=f"https://{bot.me.username}.t.me?start=start"),
                InlineKeyboardButton("Help", url=f"https://{bot.me.username}.t.me?start=help")
            ]])
        )
    except Exception as e:
        logger.error(e)
    
    logger.info("App Started...!")

    # Run Server - This need to run at the end otherwise it will stuck the bot process
    await keep_server_alive()
    # await idle()


async def main():
    # Need to load before bot.run()
    load_plugins()

    try:
        await bot.start()
        await app_init()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
