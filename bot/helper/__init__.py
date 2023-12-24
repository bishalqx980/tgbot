import asyncio
from bot import bot
from telegram import BotCommand

async def set_bot_command():
    commands = [
        BotCommand("start", "..."),
        BotCommand("echo", "..."),
        BotCommand("ping", "..."),
        BotCommand("calc", "..."),
        BotCommand("help", "..."),
    ]

    print("Bot commands updated!")
    await bot.set_my_commands(commands)

asyncio.get_event_loop().run_until_complete(set_bot_command())