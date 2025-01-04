import asyncio
from bot import bot, logger
from telegram import BotCommand

command_help = [
    BotCommand("help", "Show help message")
]

class BotCommandHelper:
    async def __init__(self, cmd, des):
        self.commad = cmd
        self.description = des


    async def set_bot_command():
        try:
            await bot.set_my_commands(command_help)
            logger.info("Bot commands updated!")
        except Exception as e:
            logger.error(e)

asyncio.get_event_loop().run_until_complete(BotCommandHelper.set_bot_command())
