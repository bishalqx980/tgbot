import asyncio
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger, owner_username
from bot.helper.telegram_helper import Message, Button
from bot.modules.mongodb import MongoDB
from bot.update_db import update_database
from bot.modules.github import GitHub


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    sent_msg = query.message

    async def popup(msg):
        await query.answer(msg, True)
    
    async def _check_whois():
        user_id = context.chat_data.get("user_id")
        if not user_id:
            error_msg = "Error: user_id not found!"
            logger.info(error_msg)
            await popup(error_msg)
            try:
                await query.message.delete()
            except Exception as e:
                logger.error(f"Error: {e}")
            return False
        if user.id != user_id:
            await popup("Access Denied!")
            return False
        return True

    # youtube ------------------------------------------------------------------------ Youtube
    if data == "mp4":
        context.user_data["content_format"] = data

    elif data == "mp3":
        context.user_data["content_format"] = data
    
    # -------------------------------------------------------------- Group management
    elif data == "unpin_all":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        try:
            await bot.unpin_all_chat_messages(chat_id)
            await Message.send_msg(chat_id, "All pinned messages has been unpinned successfully!")
            await query.message.delete()
        except Exception as e:
            logger.error(f"Error: {e}")
    
    elif data == "filters":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        try:
            try:
                find_group = context.chat_data["db_group_data"]
            except Exception as e:
                logger.error(f"Error: {e}")
                find_group = None
            
            if not find_group:
                find_group = await MongoDB.find_one("groups", "chat_id", chat_id)
                if find_group:
                    context.chat_data["db_group_data"] = find_group

            if find_group:
                filters = find_group.get("filters")
                msg = f"Chat filters -\n"
                if filters:
                    for keyword in filters:
                        msg += f"- {keyword}\n"
                else:
                    msg += "- No filters"

                btn_name = ["Close"]
                btn_data = ["close"]
                btn = await Button.cbutton(btn_name, btn_data)

                await Message.edit_msg(update, msg, sent_msg, btn)
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        except Exception as e:
            logger.error(f"Error: {e}")
    
    # Group management ----------------------------------------------------------------- help starts
    elif data == "group_management":
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
            "/filters » To set custom message/command\n"
            "/adminlist » See chat admins list\n"
            "/settings » Settings of chat (welcome, antibot, translate etc.)\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "ai":
        msg = (
            "Artificial intelligence functions -\n\n"
            "/imagine » Generate AI image\n"
            "/gpt » Ask any question to ChatGPT\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "misc_func":
        msg = (
            "Misc functions -\n\n"
            "/movie » Get any movie info by name/imdb_id\n"
            "/tr » Translate any language\n"
            "/decode » Decode - base64 to text\n"
            "/encode » Encode - text to base64\n"
            "/shortener » Short any url\n"
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
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "owner_func":
        msg = (
            "Bot owner functions -\n\n"
            "/broadcast » Broadcast message to bot users\n"
            "/db » See bot database\n"
            "/bsetting » See bot settings\n"
            "/shell » Use system shell\n"
            "/render » Render functions\n"
            "/sys » See system info\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "github_stats":
        github_repo = await MongoDB.get_data("bot_docs", "github_repo")
        latest_commit = GitHub.get_latest_commit("bishalqx980", "tgbot")
        if latest_commit:
            l_c_sha = latest_commit.get("sha")
            l_c_commit = latest_commit.get("commit") # not for use
            l_c_message = l_c_commit.get("message")
            l_c_author = l_c_commit.get("author") # not for use
            l_c_aname = l_c_author.get("name")
            l_c_date = l_c_author.get("date")
            l_c_link = f"https://github.com/bishalqx980/tgbot/commit/{l_c_sha}"

            msg = (
                f"<b>» Original repo [ <a href='{l_c_link}'>latest commit</a> ]</b>\n"
                f"<b>Last update:</b> <code>{l_c_date}</code>\n"
                f"<b>Commit:</b> <code>{l_c_message}</code>\n"
                f"<b>Committed by:</b> <code>{l_c_aname}</code>\n"
            )
        else:
            msg = "Something went wrong!"

        if github_repo:
            try:
                parse_url = urlparse(github_repo)
                split_all = parse_url.path.strip("/").split("/")
                username, repo_name = split_all

                bot_repo_commit = GitHub.get_latest_commit(username, repo_name)

                b_r_sha = bot_repo_commit.get("sha")
                b_r_commit = bot_repo_commit.get("commit") # not for use
                b_r_message = b_r_commit.get("message")
                b_r_author = b_r_commit.get("author") # not for use
                b_r_aname = b_r_author.get("name")
                b_r_date = b_r_author.get("date")
                b_r_link = f"https://github.com/{username}/{repo_name}/commit/{b_r_sha}"
                
                msg = (
                    msg + f"\n<b>» Bot repo [ <a href='{b_r_link}'>commit</a> ]</b>\n"
                    f"<b>Last update:</b> <code>{b_r_date}</code>\n"
                    f"<b>Commit:</b> <code>{b_r_message}</code>\n"
                    f"<b>Committed by:</b> <code>{b_r_aname}</code>\n"
                )

                if l_c_sha != b_r_sha:
                    msg += "\n<i>The bot repo isn't updated to the latest commit! ⚠</i>"
                else:
                    msg += "\n<i>The bot repo is updated to the latest commit...</i>"
            except Exception as e:
                logger.error(f"Error: {e}")
        
        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "help_menu":
        msg = (
            f"Hi! Welcome to the bot help section...\n"
            f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
            f"/start - to start the bot\n"
            f"/help - to see this message"
        )

        btn_name_row1 = ["Group Management", "Artificial intelligence"]
        btn_data_row1 = ["group_management", "ai"]

        btn_name_row2 = ["misc", "Bot owner"]
        btn_data_row2 = ["misc_func", "owner_func"]

        btn_name_row3 = ["GitHub", "Close"]
        btn_data_row3 = ["github_stats", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    # ---------------------------------------------------------------------------- help ends
    # bot settings ------------------------------------------------------------- bsettings starts
    elif data == "bot_pic":
        edit_cname = "bot_docs"
        find_data = "_id"
        match_data = await MongoDB.find(edit_cname, find_data)
        bot_pic = await MongoDB.get_data(edit_cname, "bot_pic")

        context.chat_data["edit_cname"] = edit_cname
        context.chat_data["find_data"] = find_data
        context.chat_data["match_data"] = match_data[0]
        context.chat_data["edit_data_name"] = "bot_pic"

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Bot pic: <code>{bot_pic}</code>\n\n"
            "<i>Note: Send an image url/link to set bot pic!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "welcome_img":
        welcome_img = await MongoDB.get_data("bot_docs", "welcome_img")

        context.chat_data["edit_data_name"] = "welcome_img"

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Welcome img: {welcome_img}\n\n"
            "<i>Note: Should bot show bot_pic on start?</i>"
        )

        btn_name_row1 = ["Yes", "No"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "images":
        edit_cname = "bot_docs"
        find_data = "_id"
        match_data = await MongoDB.find(edit_cname, find_data)
        images = await MongoDB.get_data(edit_cname, "images")

        context.chat_data["edit_cname"] = edit_cname
        context.chat_data["find_data"] = find_data
        context.chat_data["match_data"] = match_data[0]
        context.chat_data["edit_data_name"] = "images"

        if images:
            if len(images) > 20:
                storage, count_image = "", 0
                for image in images:
                    storage += f"{image},"
                    count_image += 1
                    if count_image == 20:
                        await Message.send_msg(user.id, f"{storage}")
                        storage, count_image = "", 0
                await Message.send_msg(user.id, f"{storage}")
                images = "Value sent below!"
        
        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"images: <code>{images}</code>\n\n"
            "<i>Note: Single image or Upload multiple image link separated by comma!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "support_chat":
        edit_cname = "bot_docs"
        find_data = "_id"
        match_data = await MongoDB.find(edit_cname, find_data)
        support_chat = await MongoDB.get_data(edit_cname, "support_chat")

        context.chat_data["edit_cname"] = edit_cname
        context.chat_data["find_data"] = find_data
        context.chat_data["match_data"] = match_data[0]
        context.chat_data["edit_data_name"] = "support_chat"

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Support Chat (link): <code>{support_chat}</code>\n"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "server_url":
        edit_cname = "bot_docs"
        find_data = "_id"
        match_data = await MongoDB.find(edit_cname, find_data)
        server_url = await MongoDB.get_data(edit_cname, "server_url")

        context.chat_data["edit_cname"] = edit_cname
        context.chat_data["find_data"] = find_data
        context.chat_data["match_data"] = match_data[0]
        context.chat_data["edit_data_name"] = "server_url"

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Server url: <code>{server_url}</code>\n\n"
            "<i>Note: Bot will fall asleep if you deployed the bot on render (free) and don't set this value...</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "github_repo":
        edit_cname = "bot_docs"
        find_data = "_id"
        match_data = await MongoDB.find(edit_cname, find_data)
        github_repo = await MongoDB.get_data(edit_cname, "github_repo")

        context.chat_data["edit_cname"] = edit_cname
        context.chat_data["find_data"] = find_data
        context.chat_data["match_data"] = match_data[0]
        context.chat_data["edit_data_name"] = "github_repo"

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"GitHub repo: <code>{github_repo}</code>\n\n"
            f"<i>Note: Your bot github repo link, to keep track on updates on latest repo...</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "restore_db":
        msg = (
            "<b>Bot Settings</b> -\n\n"
            "Which data will be deleted? ⚠\n"
            "- All bot setting\n\n"
            "Which data won't be deleted?\n"
            "- Bot users/groups data\n\n"
            f"<i>Note: This will erase all bot data/settings from database and restore data/settings from <code>config.env</code></i>"
        )

        btn_name_row1 = ["⚠ Restore Database"]
        btn_data_row1 = ["confirm_restore_db"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "confirm_restore_db":
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return

        await MongoDB.delete_all_doc("bot_docs")

        res = await update_database()

        msg = "Database data has been restored successfully from <code>config.env</code>!" if res else "Something went wrong!"
        await Message.send_msg(chat_id, msg)

    elif data == "b_setting_menu":
        btn_name_row1 = ["Bot pic", "Welcome img"]
        btn_data_row1 = ["bot_pic", "welcome_img"]

        btn_name_row2 = ["Images", "Support chat"]
        btn_data_row2 = ["images", "support_chat"]

        btn_name_row3 = ["GitHub", "Server url"]
        btn_data_row3 = ["github_repo", "server_url"]

        btn_name_row4 = ["⚠ Restore Settings", "Close"]
        btn_data_row4 = ["restore_db", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)

        btn = row1 + row2 + row3 + row4
        
        await Message.edit_msg(update, "<b>Bot Settings</b>", sent_msg, btn)
    # ---------------------------------------------------------------------------- bsettings ends
    # chat setting -------------------------------------------------------------- Chat settings starts
    elif data == "lang":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        try:
            _bot = context.bot_data["db_bot_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find = await MongoDB.find("bot_docs", "_id")
            _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
            context.bot_data["db_bot_data"] = _bot
        
        lang = find_chat.get("lang")
        context.chat_data["edit_data_name"] = "lang"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"language code: <code>{lang}</code>\n\n"
            "<i>Note: Get your country language code from the below link!\neg. English language code is <code>en</code></i>"
        )

        btn_name_row1 = ["Language code's"]
        btn_url_row1 = ["https://telegra.ph/Language-Code-12-24"]

        btn_name_row2 = ["Edit Value"]
        btn_data_row2 = ["edit_value"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["c_setting_menu", "close"]

        row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "auto_tr":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        auto_tr = find_chat.get("auto_tr")

        context.chat_data["edit_data_name"] = "auto_tr"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Auto translate: <code>{auto_tr}</code>\n\n"
            "<i>Note: This will automatically translate chat conversation into chat default language!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "set_echo":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        echo = find_chat.get("echo")

        context.chat_data["edit_data_name"] = "echo"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Echo: <code>{echo}</code>\n\n"
            "<i>Note: This will repeat user message!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "welcome_msg":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        welcome_msg = find_chat.get("welcome_msg")

        context.chat_data["edit_data_name"] = "welcome_msg"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Welcome user: <code>{welcome_msg}</code>\n\n"
            "<i>Note: This will welcome the new chat member!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Set custom message"]
        btn_data_row2 = ["set_custom_msg"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "set_custom_msg":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        custom_welcome_msg = find_chat.get("custom_welcome_msg")

        context.chat_data["edit_data_name"] = "custom_welcome_msg"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Welcome message\n--------------------\n<code>{custom_welcome_msg}</code>\n\n"
            "<i>Note: This message will be send as greeting message in the chat when a user join!</i>"
        )

        btn_name_row1 = ["Text formats", "Set custom message"]
        btn_data_row1 = ["text_formats", "edit_value"]

        btn_name_row2 = ["Set default message"]
        btn_data_row2 = ["remove_value"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["welcome_msg", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "text_formats":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        msg = (
            "<blockquote>Formatting</blockquote>\n"
            "<code>{first}</code>: The user's firstname\n"
            "<code>{last}</code>: The user's lastname\n"
            "<code>{fullname}</code>: The user's fullname\n"
            "<code>{username}</code>: The user's username\n"
            "<code>{mention}</code>: To mention the user\n"
            "<code>{id}</code>: The user's ID\n"
            "<code>{chatname}</code>: Chat title\n\n"
            "Example: <code>Hi {mention}, welcome to {chatname}</code>\n"
        )

        btn_name = ["Close"]
        btn_data = ["close"]
        
        btn = await Button.cbutton(btn_name, btn_data)
        
        await Message.send_msg(chat_id, msg, btn)

    elif data == "goodbye_msg":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        goodbye_msg = find_chat.get("goodbye_msg")

        context.chat_data["edit_data_name"] = "goodbye_msg"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Goodbye user: <code>{goodbye_msg}</code>\n\n"
            "<i>Note: This will send a farewell message to chat when a user left!\n</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "antibot":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        antibot = find_chat.get("antibot")

        context.chat_data["edit_data_name"] = "antibot"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Antibot: <code>{antibot}</code>\n\n"
            "<i>Note: This will prevent other bot from joining in chat!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "del_cmd":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        del_cmd = find_chat.get("del_cmd")

        context.chat_data["edit_data_name"] = "del_cmd"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Delete cmd: <code>{del_cmd}</code>\n\n"
            "<i>Note: This will delete bot commands when you will send a command in chat!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "log_channel":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        context.chat_data["edit_data_name"] = "log_channel"

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        log_channel = find_chat.get("log_channel")

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Log channel: <code>{log_channel}</code>\n\n"
            "<i>Note: This will log every actions occurred in your chat (ban, kick, mute, etc.) using bot!\nAdd the bot in a channel as admin where you want to log, then you will get a message with chat_id from bot, pass the chat_id using edit value!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "del_links":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")

        context.chat_data["edit_data_name"] = "del_links"

        try:
            find_chat = context.chat_data["db_chat_data"]
        except Exception as e:
            logger.error(f"Error: {e}")
            find_chat = None
        
        if not find_chat:
            find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
            if find_chat:
                context.chat_data["db_chat_data"] = find_chat
            else:
                await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                await query.message.delete()
                return
        
        del_links = find_chat.get("del_links")

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Delete links: <code>{del_links}</code>\n\n"
            "<i>Note: This will delete links in chat and send it converting into base64!</i>\n"
            "<i>More options coming soon...</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "c_setting_menu":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return

        if edit_cname == "groups":
            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Anti bot"]
            btn_data_row2 = ["set_echo", "antibot"]

            btn_name_row3 = ["Welcome", "Goodbye"]
            btn_data_row3 = ["welcome_msg", "goodbye_msg"]

            btn_name_row4 = ["Delete cmd", "Log channel"]
            btn_data_row4 = ["del_cmd", "log_channel"]

            btn_name_row5 = ["Delete links", "Close"]
            btn_data_row5 = ["del_links", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
            row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

            btn = row1 + row2 + row3 + row4 + row5

        elif edit_cname == "users":
            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Close"]
            btn_data_row2 = ["set_echo", "close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

            btn = row1 + row2
        
        else:
            logger.info("Error: edit_cname not found!")
            await query.message.delete()
            return
        
        await Message.edit_msg(update, "<b>Chat Settings</b> -\n\n<i>Note: Can't show full info in back menu for some technical problem!</i>", sent_msg, btn)
    # ---------------------------------------------------------------------------- chat settings ends
    # global ----------------------------------------------------------------- Global
    elif data == "edit_value":
        """
        chat_id --> main
        edit_cname --> main / query data
        find_data --> main / query data
        match_data --> main / query data
        edit_data_name --> from query data
        new_value --> from user
        del_msg_pointer -- optional
        edit_value_del_msg -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return
        
        del_msg_1 = await Message.send_msg(chat_id, "Now send a value:")
        context.chat_data["status"] = "editing"
        await asyncio.sleep(2)

        attempt = 0

        while attempt < 10:
            new_value = context.chat_data.get("new_value")
            attempt += 1
            await asyncio.sleep(1)
            if new_value:
                break

        context.chat_data["new_value"] = None

        try:
            del_msg_2 = context.chat_data.get("edit_value_del_msg_pointer")
            del_msg = [del_msg_1, del_msg_2]
            for delete in del_msg:
                await Message.del_msg(chat_id, delete)
        except Exception as e:
            logger.error(f"Error: {e}")
        
        if not new_value:
            await popup("Timeout!")
            return
        
        # ------------------------------------------------ some exceptions
        
        elif edit_data_name == "images":
            if "," in new_value:
                storage = []
                for img in new_value.split(","):
                    storage.append(img)
                new_value = storage
            else:
                new_value = [new_value]

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, new_value)
            if edit_data_name in ["images"]:
                new_value = f"{len(new_value)} items"
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")

            db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
            context.chat_data["db_chat_data"] = db_chat_data
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "remove_value":
        """
        chat_id --> main
        edit_cname --> main / query data
        find_data --> main / query data
        match_data --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = None

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")

            db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
            context.chat_data["db_chat_data"] = db_chat_data
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "true":
        """
        chat_id --> main
        edit_cname --> main / query data
        find_data --> main / query data
        match_data --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = True

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")

            db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
            context.chat_data["db_chat_data"] = db_chat_data
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "false":
        """
        chat_id --> main
        edit_cname --> main / query data
        find_data --> main / query data
        match_data --> main / query data
        edit_data_name --> from query data
        del_msg_pointer -- optional
        """
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            await popup("Error: chat_id not found!")
            await query.message.delete()
            return
        
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        if not edit_cname:
            await popup("An error occurred! send command again then try...")
            await query.message.delete()
            return
        
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data_name = context.chat_data.get("edit_data_name") # set from query data
        new_value = False

        if not edit_data_name:
            await popup("I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, new_value)
            await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {new_value}")

            db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
            context.chat_data["db_chat_data"] = db_chat_data
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "close":
        access = await _check_whois()
        if access:
            try:
                chat_id = context.chat_data.get("chat_id")
                del_msg_pointer = context.chat_data.get("del_msg_pointer")
                await query.message.delete()
                await Message.del_msg(chat_id, del_msg_pointer)
            except Exception as e:
                logger.error(f"Error: {e}")
