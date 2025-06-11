import psutil
from time import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot import __version__, BOT_UPTIME, logger
from bot.helper import BuildKeyboard
from bot.utils.database import MongoDB
from ..core.help import HelpMenuData

async def query_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("help_menu_")

    if query_data == "menu":
        text = HelpMenuData.TEXT
        btn = BuildKeyboard.cbutton(HelpMenuData.BUTTONS)
    
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

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!\n"
            "Some command has a silent & delete function! eg. <code>/s[command]</code> & <code>/d[command]</code> » /sban or /dban etc.</blockquote>"
        )

        btn_data = [
            {"Next page ⇒": "help_menu_gm2"},
            {"Back": "help_menu_menu", "Close": "misc_close"}
        ]

        btn = BuildKeyboard.cbutton(btn_data)
    
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
            "Some command has a silent & delete function! eg. <code>/s[command]</code> & <code>/d[command]</code> » /sban or /dban etc.</blockquote>"
        )

        btn_data = [
            {"⇐ Previous page": "help_menu_gm1"},
            {"Back": "help_menu_menu", "Close": "misc_close"}
        ]

        btn = BuildKeyboard.cbutton(btn_data)
    
    elif query_data == "ai_knowledge":
        text = (
            "<blockquote><b>AI/Info Functions</b></blockquote>\n\n"
            
            "• /imagine » Generate AI image.\n"
            "• /gpt » Ask any question to AI-LLM\n\n"

            "<blockquote><b>Note:</b> Send command to get more details about the command functions!</blockquote>"
        )

        btn = BuildKeyboard.cbutton([{"Back": "help_menu_menu", "Close": "misc_close"}])
    
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
        
        btn = BuildKeyboard.cbutton([{"Back": "help_menu_menu", "Close": "misc_close"}])
    
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
        
        btn = BuildKeyboard.cbutton([{"Back": "help_menu_menu", "Close": "misc_close"}])
    
    elif query_data == "botinfo":
        await query.answer("Getting information...")

        database_info = MongoDB.info()

        i_users_data = database_info.get("users_data")
        i_chats_data = database_info.get("chats_data")

        t_users_count = i_users_data.get("quantity") if i_users_data else "Unknown"
        t_chats_count = i_chats_data.get("quantity") if i_chats_data else "Unknown"

        active_status = MongoDB.find("users_data", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        sys_uptime = timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())

        sys_days = sys_uptime.days
        sys_hours, remainder = divmod(sys_uptime.seconds, 3600)
        sys_minute = remainder / 60

        bot_uptime = timedelta(seconds=time() - BOT_UPTIME)

        bot_days = bot_uptime.days
        bot_hours, remainder = divmod(bot_uptime.seconds, 3600)
        bot_minute = remainder / 60

        text = (
            "<blockquote><code><b>» bot.info()</b></code></blockquote>\n\n"

            f"<b>• Name:</b> {context.bot.first_name}\n"
            f"<b>• ID:</b> <code>{context.bot.id}</code>\n"
            f"<b>• Username:</b> {context.bot.name}\n\n"

            f"<b>• Registered users:</b> <code>{t_users_count}</code>\n"
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n"
            f"<b>• Total chats:</b> <code>{t_chats_count}</code>\n\n"

            f"<b>• System uptime:</b> <code>{int(sys_days)}d {int(sys_hours)}h {int(sys_minute)}m</code>\n"
            f"<b>• Bot uptime:</b> <code>{int(bot_days)}d {int(bot_hours)}h {int(bot_minute)}m</code>\n"
            f"<b>• Version (stable):</b> <code>{__version__}</code>"
        )

        btn_data = [
            {"Source code": "https://github.com/bishalqx980/tgbot", "Report bug": "https://github.com/bishalqx980/tgbot/issues"},
            {"Developer": "https://t.me/bishalqx680/22"},
            {"Back": "help_menu_menu", "Close": "misc_close"}
        ]
        
        btn = BuildKeyboard.cbutton(btn_data)
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
