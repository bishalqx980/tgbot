from telegram import Update
from bot.helper.telegram_helper import Message, Button


class QueryBotHelp:
    async def _query_help_group_management(update: Update, query):
        msg = (
            "Group Moderation Commands -\n\n"
            "/id » Show chat/user id\n"
            "/invite » Generate/Get invite link\n"
            "/promote » Promote a member\n"
            "/demote » Demote a member\n"
            "/pin » Pin message loudly\n"
            "/unpin » Unpin a pinned message or all pinned messages\n"
            "/ban » Ban a member\n"
            "/unban » Unban a member\n"
            "/kick » Kick a member\n"
            "/kickme » The easy way to out\n"
            "/mute » Mute a member (member will be unable to send messages etc.)\n"
            "/unmute » Unmute a member (member will be able to send messages etc.)\n"
            "/del » Delete replied message with notifying/telling something to the member!\n"
            "/purge » Delete every messages from replied message to current message!\n"
            "/lock » Lock the chat (no one can send messages etc.)\n"
            "/unlock » Unlock the chat (back to normal)\n"
            "/filters | /filter | /remove » To see/set/remove custom message/command\n"
            "/adminlist » See chat admins list\n"
            "/settings » Settings of chat (welcome, antibot, translate etc.)\n\n"
            "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_ai(update: Update, query):
        msg = (
            "Artificial intelligence functions -\n\n"
            "/imagine » Generate AI image\n"
            "/gpt » Ask any question to ChatGPT\n\n"
            "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_misc_functions(update: Update, query):
        msg = (
            "Misc functions -\n\n"
            "/movie » Get any movie info by name/imdb_id\n"
            "/tr » Translate any language\n"
            "/decode » Decode - base64 to text\n"
            "/encode » Encode - text to base64\n"
            "/short » Short any url\n"
            "/ping » Ping any url\n"
            "/calc » Calculate any math (supported syntex: +, -, *, /)\n"
            "/webshot » Take Screenshot of any website\n"
            "/weather » Get weather info of any city\n"
            "/ytdl » Download youtube video\n"
            "/yts » Search video on youtube\n"
            "/qr » To generate a QR code\n"
            "/itl » To convert image into link\n"
            "/id » Show chat/user id\n"
            "/settings » Settings of chat\n\n"
            "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)


    async def _query_help_owner_functions(update: Update, query):
        msg = (
            "Bot owner functions -\n\n"
            "/broadcast » Broadcast message to bot users\n"
            "/db » Get bot database\n"
            "/bsettings » Get bot settings\n"
            "/shell » Use system shell\n"
            "/log » Get log file (for error handling)\n"
            "/restart » Restart the bot\n"
            "/sys » Get system info\n\n"
            "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["query_help_menu", "query_close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, query.message, btn)
