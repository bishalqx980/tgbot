import asyncio
from bot import bot, logger
from telegram import BotCommand

commands = [
    BotCommand("start", "Start the bot"),
    BotCommand("movie", "Get any movie info by name/imdb id"),
    BotCommand("tr", "Translate any lang"),
    BotCommand("setlang", "Set chat default language"),
    BotCommand("decode", "Decode base64"),
    BotCommand("encode", "Encode text"),
    BotCommand("shortener", "Short any url"),
    BotCommand("ping", "Ping any url"),
    BotCommand("calc", "Calculate any math"),
    BotCommand("echo", "Make chat fun"),
    BotCommand("webshot", "Take Screenshot of any website"),
    BotCommand("weather", "Get weather info"),
    BotCommand("imagine", "AI Image generator"),
    BotCommand("gpt", "ChatGPT AI for your chat"),
    BotCommand("ytdl", "Download youtube video"),
    BotCommand("yts", "Search video on youtube"),
    BotCommand("stats", "Show your config data"),
    BotCommand("id", "Show chat/user id"),
    BotCommand("welcome", "Set welcome msg in group"),
    BotCommand("goodbye", "Set goodbye msg in group"),
    BotCommand("antibot", "Restrict other bots from joining in group"),
    BotCommand("invite", "Generate invite link for Group"),
    BotCommand("pin", "Pin message loudly"),
    BotCommand("unpin", "Unpin a pinned message"),
    BotCommand("ban", "Ban an user from group"),
    BotCommand("unban", "Unban an user from group"),
    BotCommand("kick", "Kick an user from group"),
    BotCommand("kickme", "The easy way to out"),
    BotCommand("mute", "Mute an user (Restrict from group)"),
    BotCommand("unmute", "Unmute an user (Unrestrict from group)"),
    BotCommand("lockchat", "Lockdown the group"),
    BotCommand("unlockchat", "Unlock the group"),
    BotCommand("adminlist", "See group admins list"),
    BotCommand("help", "Show help message"),
    BotCommand("broadcast", "owner only"),
    BotCommand("database", "owner only"),
    BotCommand("bsetting", "owner only"),
    BotCommand("shell", "owner only"),
    BotCommand("render", "owner only"),
    BotCommand("sys", "owner only")
]

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
