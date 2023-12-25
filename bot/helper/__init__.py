import asyncio
from bot import bot
from telegram import BotCommand

async def set_bot_command():
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("movie", "Get any movie info"),
        BotCommand("tr", "Translate text"),
        BotCommand("setlang", "Set chat language"),
        BotCommand("decode", "Decode base64 code"),
        BotCommand("encode", "Encode text code"),
        BotCommand("shortener", "Short any url"),
        BotCommand("ping", "Ping any url"),
        BotCommand("calc", "Calculate any math"),
        BotCommand("echo", "Make chat fun"),
        BotCommand("help", "Show help message"),
        BotCommand("broadcast", "owner only"),
        BotCommand("database", "owner only")
    ]

    print("Bot commands updated!")
    await bot.set_my_commands(commands)

asyncio.get_event_loop().run_until_complete(set_bot_command())