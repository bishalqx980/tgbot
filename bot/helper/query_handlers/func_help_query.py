from telegram import Update
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


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

        btn_data_row1 = {
            "Next page >>": "query_help_group_management_p2"
        }

        btn_data_row2 = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

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

        btn_data_row1 = {
            "<< Previous page": "query_help_group_management_p1"
        }

        btn_data_row2 = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        row1 = await Button.cbutton(btn_data_row1)
        row2 = await Button.cbutton(btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_ai(update: Update, query):
        msg = (
            "<b>Artificial intelligence</b>\n\n"
            "<b>⚠️ Disabled due to limitations. They may be reintroduced in future updates.</b>\n\n"
            "<s>/imagine » generate AI image</s>\n"
            "<s>/gpt » ask any question to ChatGPT</s>\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_data = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        btn = await Button.cbutton(btn_data, True)
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
            "/weather » get weather info of any city\n"
            "/qr » generate a QR code\n"
            "/itl » convert image into a public link\n"
            "/paste » paste your text in telegraph & get public link\n"
            "/whisper » secretly tell something to someone in group chat\n"
            "/id » show chat/user id\n"
            "/info » show user info\n"
            "/psndl » search ps3 & some other playstation games link (mostly ps3)\n"
            "/rap » generate rap from <code>rap_data</code> (use /psndl to get rap data)\n"
            "/settings » settings of chat\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_data = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        btn = await Button.cbutton(btn_data, True)
        await Message.edit_message(update, msg, query.message, btn)


    async def _query_help_owner_functions(update: Update, query):
        msg = (
            "<b>Bot owner functions</b>\n\n"
            "/broadcast » broadcast message to all active users\n"
            "/send » send message to specified chat_id\n"
            "/database » get bot database\n"
            "/bsettings » get bot settings\n"
            "/shell » use system shell\n"
            "/log » get log file (for error handling)\n"
            "/sys » get system info\n\n"
            "<i><b>Note:</b> Send command to get more details about the command functions!</i>"
        )

        btn_data = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        btn = await Button.cbutton(btn_data, True)
        await Message.edit_message(update, msg, query.message, btn)
    

    async def _query_help_bot_info(update: Update, query):
        _bot_info = await LOCAL_DATABASE.find("_bot_info")
        info_db = await MongoDB.info_db()
        for i in info_db:
            if i[0] == "users":
                total_users = i[1]
                break
            else:
                total_users = "~"
        
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        msg = (
            "<b><code>» bot.info()</code></b>\n\n"

            f"<b>• Name:</b> {_bot_info.get('full_name')}\n"
            f"<b>• ID:</b> <code>{_bot_info.get('id')}</code>\n"
            f"<b>• Username:</b> {_bot_info.get('name')}\n\n"

            f"<b>• Registered users:</b> <code>{total_users}</code>\n"
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
        )

        btn_data = {
            "Back": "query_help_menu",
            "Close": "query_close"
        }

        btn = await Button.cbutton(btn_data, True)
        await Message.edit_message(update, msg, query.message, btn)
