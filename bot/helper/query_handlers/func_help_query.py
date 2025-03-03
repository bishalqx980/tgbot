import time
import json
import psutil
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ChatAction
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB


class QueryBotHelp:
    async def _query_help_group_management_p1(update: Update, query):
        msg = (
            "<b>Group Moderation Commands | p:1</b>\n\n"
            "/id » Show chat/user id\n"
            "/invite » Generate chat invite link\n"
            "/promote | /fpromote » promote a member ('f' means with full privilege)\n"
            "/apromote | /fapromote » <code>anonymously</code> promote/fpromote a member\n"
            "/admintitle » set admin custom title\n"
            "/demote » demote a member\n"
            "/pin » pin replied message loudly\n"
            "/unpin » unpin a pinned message\n"
            "/unpinall » unpin all pinned messages"
            "/ban » ban a member\n"
            "/unban » unban a member\n"
            "/kick » kick a member\n"
            "/kickme » The easy way to out\n"
            "/mute » restrict a member (member will be unable to send messages etc.)\n"
            "/unmute » unrestrict a restricted member\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</i>"
        )

        btn_data = [
            {"Next page →": "query_help_group_management_p2"},
            {"Back": "query_help_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_group_management_p2(update: Update, query):
        msg = (
            "<b>Group Moderation Commands | p:2</b>\n\n"
            "/del » delete the replied message with a warning!\n"
            "/purge » delete every messages from replied to current message!\n"
            "/purgefrom | /purgeto » delete every messages between <code>purgefrom</code> and <code>purgeto</code> replied message!\n"
            "/lock » lock the chat (member will be unable to send messages etc.)\n"
            "/unlock » unlock the chat (back to normal)\n"
            "/filters | /filter | /remove » to see/set/remove custom message/command\n"
            "/adminlist » to see chat admins list\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</i>"
        )

        btn_data = [
            {"← Previous page": "query_help_group_management_p1"},
            {"Back": "query_help_menu", "Close": "query_close"}
        ]

        btn = await Button.cbutton(btn_data)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_ai(update: Update, query):
        msg = (
            "<b>Artificial intelligence</b>\n\n"
            "/imagine » generate AI image\n"
            "/gpt » ask any question to ChatGPT\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn = await Button.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_misc_functions(update: Update, query):
        msg = (
            "<b>Misc functions</b>\n\n"
            "/movie » get any movie info by name or imdb id\n"
            "/tr » translate any language\n"
            "/decode » convert base64 into text\n"
            "/encode » convert text into base64\n"
            "/short » short any url\n"
            "/ping » ping any url\n"
            "/calc » calculate any math (supported syntex: +, -, *, /)\n"
            "/tts » convert text into speech\n"
            "/weather » get weather info of any city\n"
            "/qr » generate a QR code\n"
            "/itl » convert image into a public link\n"
            "/paste » paste your text in telegraph & get public link\n"
            "/whisper » secretly tell something to someone in group chat\n"
            "/ytdl » download audio/song from youtube\n"
            "/id » show chat/user id\n"
            "/info » show user info\n"
            "/psndl » search ps3 & some other playstation games link (mostly ps3)\n"
            "/rap » generate rap from <code>rap_data</code> (use /psndl to get rap data)\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )
        
        btn = await Button.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_owner_functions(update: Update, query):
        msg = (
            "<b>Bot owner functions</b>\n\n"
            "/broadcast » broadcast message to all active users\n"
            "/send » send message to specified chat_id\n"
            "/database » get bot/chat database\n"
            "/bsettings » get bot settings\n"
            "/shell » use system shell\n"
            "/log » get log file (for error handling)\n"
            "/sys » get system info\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )
        
        btn = await Button.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_help_bot_info(update: Update, query):
        # giving a delay notification :)
        try:
            await update.effective_chat.send_action(ChatAction.TYPING)
        except:
            pass

        database_info = await MongoDB.info_db()
        total_users = None
        total_groups = None

        for info in database_info:
            info = database_info[info]
            if info.get("name") == "users":
                total_users = info.get("quantity")
            elif info.get("name") == "groups":
                total_groups = info.get("quantity")
            
            if total_users and total_groups:
                break
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)
        # Calculate the system uptime
        sys_uptime = timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())
        # Extracting system uptime in days, hours and minutes
        sys_days = sys_uptime.days
        sys_hours, remainder = divmod(sys_uptime.seconds, 3600)
        sys_minute = remainder / 60
        # Getting bot uptime
        bot_uptime = timedelta(seconds=time.time() - float(open("sys/bot_uptime.txt", "r").read()))
        # Extracting bot uptime in days, hours and minutes
        bot_days = bot_uptime.days
        bot_hours, remainder = divmod(bot_uptime.seconds, 3600)
        bot_minute = remainder / 60
        # loading bot_commands file
        bot_commands = json.load(open("sys/bot_commands.json", "r"))
        bot_commands = bot_commands.get("bot_commands")

        msg = (
            "<blockquote><code><b>» bot.info()</b></code></blockquote>\n\n"

            f"<b>• Name:</b> {bot.first_name}\n"
            f"<b>• ID:</b> <code>{bot.id}</code>\n"
            f"<b>• Username:</b> {bot.name}\n\n"

            f"<b>• Registered users:</b> <code>{total_users}</code>\n"
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n"
            f"<b>• Total chats:</b> <code>{total_groups}</code>\n\n"

            f"<b>• System uptime:</b> <code>{int(sys_days)}d {int(sys_hours)}h {int(sys_minute)}m</code>\n"
            f"<b>• Bot uptime:</b> <code>{int(bot_days)}d {int(bot_hours)}h {int(bot_minute)}m</code>\n"
            f"<b>• Total commands:</b> <code>{len(bot_commands)}</code>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
        )
        
        btn = await Button.cbutton([{"Back": "query_help_menu", "Close": "query_close"}])
        await Message.edit_message(update, msg, query.message, btn)
