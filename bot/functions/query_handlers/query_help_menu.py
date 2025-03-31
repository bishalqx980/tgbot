import psutil
from time import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB, MongoDB

async def query_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("help_menu_")

    if query_data == "menu":
        text = (
            "<blockquote><b>Help Menu</b></blockquote>\n\n"
            "Hey! Welcome to the bot help section.\n"
            "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
            "• /start - Start the bot\n"
            "• /help - To see this message\n\n"
            "<blockquote><b>Note:</b> The bot is compatible with the <code>/</code>, <code>!</code>, <code>.</code> and <code>-</code> command prefixes.</blockquote>"
        )

        btn_data = [
            {"Group Management": "help_menu_gm1", "AI": "help_menu_ai"},
            {"Misc": "help_menu_misc", "Owner/Sudo": "help_menu_owner"},
            {"» bot.info()": "help_menu_botinfo", "Close": "help_menu_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "gm1":
        text = (
            "<blockquote><b>Group Management</b></blockquote>\n\n"

            "• /id » Show chat/user id\n"
            "• /invite » Generate chat invite link\n"
            "• /promote » Promote chat member\n"
            "• /demote » Demote chat member\n"
            "• /pin » Pin replied message\n"
            "• /unpin » Unpin a pinned message\n"
            "• /unpinall » Unpin all pinned messages\n"
            "• /ban » Ban chat member\n"
            "• /unban » Unban chat member\n"
            "• /kick » Kick chat member\n"
            "• /kickme » The easy way to out\n"
            "• /mute » Restrict a member (member will be unable to send messages etc.)\n"
            "• /unmute » Unrestrict a restricted member\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</blockquote>"
        )

        btn_data = [
            {"Next page ⇒": "help_menu_gm2"},
            {"Back": "help_menu_menu", "Close": "help_menu_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "gm2":
        text = (
            "<blockquote><b>Group Management</b></blockquote>\n\n"

            "• /purge » Delete all messages between replied to current message!\n"
            "• /purgefrom | /purgeto » Delete all messages between <code>purgefrom</code> and <code>purgeto</code>.\n"
            "• /lock » Lock the chat (member will be unable to send messages etc.)\n"
            "• /unlock » Unlock the chat (back to normal)\n"
            "• /adminlist » Get chat admins list.\n"
            "• /filters | /filter | /remove » to see/set/remove custom message/command.\n"
            "• /settings » Settings of chat\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent function! eg. <code>/s[command]</code> » /sban etc.</blockquote>"
        )

        btn_data = [
            {"⇐ Previous page": "help_menu_gm1"},
            {"Back": "help_menu_menu", "Close": "help_menu_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "ai":
        text = (
            "<blockquote><b>AI Functions</b></blockquote>\n\n"

            "• /imagine » Generate AI image.\n"
            "• /gpt » Ask any question to AI-LLM\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!</blockquote>"
        )

        btn = ButtonMaker.cbutton([{"Back": "help_menu_menu", "Close": "help_menu_close"}])
    
    elif query_data == "misc":
        text = (
            "<blockquote><b>Misc Functions</b></blockquote>\n\n"

            "• /movie » Get Movie info by name or IMDB ID\n"
            "• /tr » Google translator\n"
            "• /decode » Convert base64 into text\n"
            "• /encode » Convert text into base64\n"
            "• /shorturl » Short URL (shrinkme)\n"
            "• /ping » Get response of website\n"
            "• /calc » Normal calculator (supported syntex: +, -, *, /)\n"
            "• /tts » Convert text into speech (voice)\n"
            "• /weather » Get current weather info\n"
            "• /qr » Generate QR code (image)\n"
            "• /imgtolink » Get Image to public link\n"
            "• /paste » Paste replied text in telegraph (returns link)\n"
            "• /whisper » Whisper someone in public chat (secretly)\n"
            "• /ytdl » Download audio/song from youtube\n"
            "• /id » Show chat/user id\n"
            "• /info » Show user info\n"
            "• /psndl » Get playstation (psn/.pkg) games/updates/dlc link (mostly ps3)\n"
            "• /rap » Generate .rap file <code>hex_code</code> (LICENSE file for PSN file, /psndl to get hex code)\n"
            "• /settings » Settings of chat\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!</blockquote>"
        )
        
        btn = ButtonMaker.cbutton([{"Back": "help_menu_menu", "Close": "help_menu_close"}])
    
    elif query_data == "owner":
        text = (
            "<blockquote><b>Owner/Sudo Functions</b></blockquote>\n\n"

            "• /say » Send message as bot\n"
            "• /broadcast » Broadcast message to all active users\n"
            "• /send » Send message to specified ChatID\n"
            "• /cadmins » Get adminlist of specified ChatID\n"
            "• /invitelink » Get invite link of specified ChatID\n"
            "• /database » Get bot or specified chat database info\n"
            "• /bsettings » Get bot settings\n"
            "• /shell » Access/Use system shell\n"
            "• /log » Get log file (for error handling)\n"
            "• /sys » Get system info\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!</blockquote>"
        )
        
        btn = ButtonMaker.cbutton([{"Back": "help_menu_menu", "Close": "help_menu_close"}])
    
    elif query_data == "botinfo":
        await query.answer("Getting information...")

        database_info = MongoDB.info()
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
        
        active_status = MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        sys_uptime = timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())

        sys_days = sys_uptime.days
        sys_hours, remainder = divmod(sys_uptime.seconds, 3600)
        sys_minute = remainder / 60

        bot_uptime = timedelta(seconds=time() - float(MemoryDB.bot_data.get("bot_uptime") or 0))

        bot_days = bot_uptime.days
        bot_hours, remainder = divmod(bot_uptime.seconds, 3600)
        bot_minute = remainder / 60

        bot_commands = MemoryDB.bot_data.get("bot_commands") or []

        text = (
            "<blockquote><code><b>» bot.info()</b></code></blockquote>\n\n"

            f"<b>• Name:</b> {context.bot.first_name}\n"
            f"<b>• ID:</b> <code>{context.bot.id}</code>\n"
            f"<b>• Username:</b> {context.bot.name}\n\n"

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
        
        btn = ButtonMaker.cbutton([{"Back": "help_menu_menu", "Close": "help_menu_close"}])
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(user.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
