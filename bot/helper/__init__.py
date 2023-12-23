from bot import bot
from telegram import BotCommand

async def set_bot_command():
    commands = [
        BotCommand("start", "..."),
        BotCommand("echo", "..."),
        BotCommand("ping", "..."),
        BotCommand("calc", "..."),
    ]

    print("Bot commands updated!")
    await bot.set_my_commands(commands)
