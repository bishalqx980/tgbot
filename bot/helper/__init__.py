import asyncio
from bot import bot, logger
from telegram import BotCommand

# commands = [
#     BotCommand("start", "Start the bot")
# ]

command_help = [
    BotCommand("help", "Show help message")
]

class BotCommandHelper:
    async def __init__(self, cmd, des):
        self.commad = cmd
        self.description = des


    async def set_bot_command():
        await bot.set_my_commands(command_help)
        logger.info("🤖 Bot commands updated!")


asyncio.get_event_loop().run_until_complete(BotCommandHelper.set_bot_command())
