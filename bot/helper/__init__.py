import asyncio
from bot import bot
from telegram import BotCommand

commands = [
    BotCommand("start", "Start the bot"),
    BotCommand("movie", "Get any movie info by name/imdb id"),
    BotCommand("tr", "Translate any lang to your lang"),
    BotCommand("setlang", "Set chat default language"),
    BotCommand("decode", "Decode base64 code"),
    BotCommand("encode", "Encode text code"),
    BotCommand("shortener", "Short any url"),
    BotCommand("ping", "Ping any url"),
    BotCommand("calc", "Calculate any math"),
    BotCommand("echo", "Make chat fun"),
    BotCommand("ban", "Ban an user from group"),
    BotCommand("unban", "Unban an user from group"),
    BotCommand("kick", "Kick an user from group"),
    BotCommand("mute", "Mute an user (Restrict from group)"),
    BotCommand("unmute", "Unmute an user (Unrestrict from group)"),
    BotCommand("help", "Show help message"),
    BotCommand("broadcast", "owner only"),
    BotCommand("database", "owner only")
]

class BotCommandHelper:
    def __init__(self, cmd, des):
        self.commad = cmd
        self.description = des


    async def set_bot_command():
        await bot.set_my_commands(commands)
        print("🤖 Bot commands updated!")


asyncio.get_event_loop().run_until_complete(BotCommandHelper.set_bot_command())