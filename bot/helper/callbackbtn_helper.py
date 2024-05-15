import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.mongodb import MongoDB
from bot.update_db import update_database


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
            await query.message.delete()
            return False
        
        if user.id != user_id:
            await popup("Access Denied!")
            return False
        
        return True


    # youtube
    if data == "mp4":
        context.user_data["content_format"] = data

    elif data == "mp3":
        context.user_data["content_format"] = data
    
    # Group management
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
            "/lock » Lock the chat (no one can send messages etc.)\n"
            "/unlock » Unlock the chat (back to normal)\n"
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
            "/settings » Settings of chat\n"
            "/id » Show chat/user id\n\n"
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
            "/database » See bot database\n"
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

        btn_name_row3 = ["Close"]
        btn_data_row3 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)

    elif data == "unpin_all":
        access = await _check_whois()
        if not access:
            return
        
        # importing from group_management
        from bot.modules.group_management import exe_func_unpin_all_msg
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        await query.message.delete()
        await exe_func_unpin_all_msg(update, context, chat_id)
    
    # bot settings
    elif data == "bot_pic":
        bot_pic = await MongoDB.get_data("bot_docs", "bot_pic")

        context.chat_data["edit_data"] = "bot_pic"
        context.chat_data["old_value"] = bot_pic

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Bot pic: <code>{bot_pic}</code>\n"
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

        context.chat_data["edit_data"] = "welcome_img"

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
    
    elif data == "telegraph":
        telegraph = await MongoDB.get_data("bot_docs", "telegraph")

        context.chat_data["edit_data"] = "telegraph"
        context.chat_data["old_value"] = telegraph

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Telegraph link: <code>{telegraph}</code>\n"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "images":
        images = await MongoDB.get_data("bot_docs", "images")
        
        context.chat_data["edit_data"] = "images"
        context.chat_data["old_value"] = images

        if images:
            if len(images) > 10:
                storage, count_image = "", 0
                for image in images:
                    storage += f"{image},"
                    count_image += 1
                    if count_image == 10:
                        count_image = 0
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

    elif data == "lang_code_list":
        lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")

        context.chat_data["edit_data"] = "lang_code_list"
        context.chat_data["old_value"] = lang_code_list

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Language code list (link): <code>{lang_code_list}</code>\n"
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
        support_chat = await MongoDB.get_data("bot_docs", "support_chat")

        context.chat_data["edit_data"] = "support_chat"
        context.chat_data["old_value"] = support_chat

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
        server_url = await MongoDB.get_data("bot_docs", "server_url")

        context.chat_data["edit_data"] = "server_url"
        context.chat_data["old_value"] = server_url

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
    
    elif data == "chatgpt_limit":
        chatgpt_limit = await MongoDB.get_data("bot_docs", "chatgpt_limit")
        usage_reset = await MongoDB.get_data("bot_docs", "usage_reset")

        context.chat_data["edit_data"] = "chatgpt_limit"
        context.chat_data["old_value"] = chatgpt_limit

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"ChatGPT usage limit: <code>{chatgpt_limit}</code>\n\n"
            f"<i>Note: This limit is for other users! Will be reset after {usage_reset}hour!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "ai_imagine_limit":
        ai_imagine_limit = await MongoDB.get_data("bot_docs", "ai_imagine_limit")
        usage_reset = await MongoDB.get_data("bot_docs", "usage_reset")

        context.chat_data["edit_data"] = "ai_imagine_limit"
        context.chat_data["old_value"] = ai_imagine_limit

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"AI imagine usage limit: <code>{ai_imagine_limit}</code>\n\n"
            f"<i>Note: This limit is for other users! Will be reset after {usage_reset}hour!</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "usage_reset":
        usage_reset = await MongoDB.get_data("bot_docs", "usage_reset")

        context.chat_data["edit_data"] = "usage_reset"
        context.chat_data["old_value"] = usage_reset

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Usage reset (hour): <code>{usage_reset}</code>\n\n"
            f"<i>Note: Usage reset time for limited functions like chagpt, imagine etc. (Applicable for users)</i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "premium_seller":
        from bot import owner_username
        
        premium_seller = await MongoDB.get_data("bot_docs", "premium_seller")

        context.chat_data["edit_data"] = "premium_seller"
        context.chat_data["old_value"] = premium_seller

        if not premium_seller:
            premium_seller = owner_username

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"Premium seller: @{premium_seller}\n\n"
            f"<i>Note: Send premium seller username without @ eg. <code>bishalqx980</code></i>"
        )

        btn_name_row1 = ["Edit Value", "Remove Value"]
        btn_data_row1 = ["edit_value", "remove_value"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["b_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "premium_users":
        premium_users = await MongoDB.get_data("bot_docs", "premium_users")

        context.chat_data["edit_data"] = "premium_users"
        context.chat_data["old_value"] = premium_users

        user_count = len(premium_users) if premium_users else 0

        msg = (
            "<b>Bot Settings</b> -\n\n"
            f"<i>Total premium user {user_count}</i>\n"
            f"Premium users: {premium_users}\n\n"
            f"<i>Note: Send user ids in a list eg. <code>123456, 125123, ...</code> separated with comma | for single user id eg. <code>123456</code></i>"
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
            "- All bot setting\n"
            "- premium seller and users id\n\n"
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
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return

        await MongoDB.delete_all_doc("bot_docs")

        res = await update_database()

        msg = "Database data has been restored successfully from <code>config.env</code>!" if res else "Something went wrong!"
        await Message.send_msg(chat_id, msg)
    
    elif data == "edit_value":
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_data = context.chat_data.get("edit_data")
        old_value = context.chat_data.get("old_value")

        if not edit_data:
            await Message.send_msg(chat_id, "I don't know which data to update! Please go back and then try again!")
            return

        del_msg = await Message.send_msg(chat_id, "Now send a value:")
        context.chat_data["status"] = "editing"
        await asyncio.sleep(2)

        attempt = 0

        while attempt < 7:
            new_value = context.chat_data.get("new_value")
            attempt += 1
            await asyncio.sleep(1)
            if new_value:
                break
        
        if not new_value:
            await Message.send_msg(chat_id, "Timeout!")
            await Message.del_msg(chat_id, del_msg)
            return
        
        if edit_data == "premium_users":
            if not isinstance(new_value, int):
                if "," in new_value:
                    storage = []
                    for user_id in new_value.split(","):
                        storage.append(int(user_id))
                    new_value = storage
            else:
                new_value = [new_value]
        
        if edit_data == "images":
            if "," in new_value:
                storage = []
                for img in new_value.split(","):
                    storage.append(img)
                new_value = storage
            else:
                new_value = [new_value]
        
        if not isinstance(new_value, int) and edit_data not in ["premium_users", "images"]:
            if new_value.lower() == "true":
                new_value = True
            elif new_value.lower() == "false":
                new_value = False

        try:
            await MongoDB.update_db("bot_docs", edit_data, old_value, edit_data, new_value)
            await Message.del_msg(chat_id, del_msg)
            await Message.send_msg(chat_id, f"Database updated!\n\nData: {edit_data}\nValue: <code>{new_value}</code>") 
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.del_msg(chat_id, del_msg)
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "remove_value":
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_data = context.chat_data.get("edit_data")
        old_value = context.chat_data.get("old_value")
        new_value = None

        if not edit_data:
            await Message.send_msg(chat_id, "I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db("bot_docs", edit_data, old_value, edit_data, new_value)
            await Message.send_msg(chat_id, f"{edit_data} value set to <code>{new_value}</code>!") 
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "b_setting_menu":
        btn_name_row1 = ["Bot pic", "Welcome img"]
        btn_data_row1 = ["bot_pic", "welcome_img"]

        btn_name_row2 = ["Telegraph", "Images", "Lang code list"]
        btn_data_row2 = ["telegraph", "images", "lang_code_list"]

        btn_name_row3 = ["Support chat", "Server url"]
        btn_data_row3 = ["support_chat", "server_url"]

        btn_name_row4 = ["ChatGpt limit", "Imagine limit", "Usage reset"]
        btn_data_row4 = ["chatgpt_limit", "ai_imagine_limit", "usage_reset"]

        btn_name_row5 = ["Premium seller", "Premium users"]
        btn_data_row5 = ["premium_seller", "premium_users"]

        btn_name_row6 = ["⚠ Restore Settings", "Close"]
        btn_data_row6 = ["restore_db", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
        row6 = await Button.cbutton(btn_name_row6, btn_data_row6, True)

        btn = row1 + row2 + row3 + row4 + row5 + row6
        
        await Message.edit_msg(update, "<b>Bot Settings</b>", sent_msg, btn)
    
    # chat setting
    elif data == "lang":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        lang = await MongoDB.get_data(edit_cname, "lang")

        lang_code_list = await MongoDB.get_data("bot_docs", "lang_code_list")

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"language code: <code>{lang}</code>\n\n"
            "<i>Note: Get your country language code from the below link!\neg. English language code is <code>en</code></i>"
        )

        btn_name_row1 = ["Language code's"]
        btn_url_row1 = [lang_code_list]

        btn_name_row2 = ["Edit Value"]
        btn_data_row2 = ["set_lang"]

        btn_name_row3 = ["Back", "Close"]
        btn_data_row3 = ["c_setting_menu", "close"]

        row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

        btn = row1 + row2 + row3

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "set_lang":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname")
        find_data = context.chat_data.get("find_data")
        match_data = context.chat_data.get("match_data")
        edit_data = "lang"

        del_msg = await Message.send_msg(chat_id, "Now send a value:")
        context.chat_data["status"] = "editing"
        await asyncio.sleep(1)

        attempt = 0

        while attempt < 10:
            new_value = context.chat_data.get("new_value")
            attempt += 1
            await asyncio.sleep(1)
            if new_value:
                break
        
        if not new_value:
            await Message.send_msg(chat_id, "Timeout!")
            await Message.del_msg(chat_id, del_msg)
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data, new_value)
            await Message.del_msg(chat_id, del_msg)
            await Message.send_msg(chat_id, f"Database updated!\n\nData: {edit_data}\nValue: <code>{new_value}</code>") 
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.del_msg(chat_id, del_msg)
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "auto_tr":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")
        auto_tr = await MongoDB.get_data(edit_cname, "auto_tr")

        context.chat_data["edit_data"] = "auto_tr"

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
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await Message.send_msg(chat_id, "An error occurred! send command again then try...")
            return

        echo = await MongoDB.get_data(edit_cname, "echo")

        context.chat_data["edit_data"] = "echo"

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
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await Message.send_msg(chat_id, "An error occurred! send command again then try...")
            return

        welcome_msg = await MongoDB.get_data(edit_cname, "welcome_msg")

        context.chat_data["edit_data"] = "welcome_msg"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Welcome user: <code>{welcome_msg}</code>\n\n"
            "<i>Note: This will welcome the new chat member!</i>"
        )

        btn_name_row1 = ["Enable", "Disable"]
        btn_data_row1 = ["true", "false"]

        btn_name_row2 = ["Back", "Close"]
        btn_data_row2 = ["c_setting_menu", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "goodbye_msg":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await Message.send_msg(chat_id, "An error occurred! send command again then try...")
            return

        goodbye_msg = await MongoDB.get_data(edit_cname, "goodbye_msg")

        context.chat_data["edit_data"] = "goodbye_msg"

        msg = (
            "<b>Chat Settings</b> -\n\n"
            f"Goodbye user: <code>{goodbye_msg}</code>\n\n"
            "<i>Note: This will send a farewell message to chat when a user left!</i>"
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
        
        chat_id = context.chat_data.get("chat_id")
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname")
        if not edit_cname:
            await Message.send_msg(chat_id, "An error occurred! send command again then try...")
            return

        antibot = await MongoDB.get_data(edit_cname, "antibot")

        context.chat_data["edit_data"] = "antibot"

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

    elif data == "c_setting_menu":
        access = await _check_whois()
        if not access:
            return
        
        edit_cname = context.chat_data.get("edit_cname")

        if edit_cname == "groups":
            btn_name_row1 = ["Language", "Auto translate"]
            btn_data_row1 = ["lang", "auto_tr"]

            btn_name_row2 = ["Echo", "Anti bot"]
            btn_data_row2 = ["set_echo", "antibot"]

            btn_name_row3 = ["Welcome", "Goodbye"]
            btn_data_row3 = ["welcome_msg", "goodbye_msg"]

            btn_name_row4 = ["Close"]
            btn_data_row4 = ["close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
            row4 = await Button.cbutton(btn_name_row4, btn_data_row4)

            btn = row1 + row2 + row3 + row4

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

    # global close
    elif data == "true":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id") # set from main.py
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data = context.chat_data.get("edit_data") # set from query data
        new_value = True

        if not edit_data:
            await Message.send_msg(chat_id, "I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data, new_value)
            await Message.send_msg(chat_id, f"Database updated!\n\nData: {edit_data}\nValue: <code>{new_value}</code>") 
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")
    
    elif data == "false":
        access = await _check_whois()
        if not access:
            return
        
        chat_id = context.chat_data.get("chat_id") # set from main.py
        if not chat_id:
            logger.info("Error: chat_id not found!")
            await query.message.delete()
            return
        edit_cname = context.chat_data.get("edit_cname") # set from main.py
        find_data = context.chat_data.get("find_data") # set from main.py
        match_data = context.chat_data.get("match_data") # set from main.py
        edit_data = context.chat_data.get("edit_data") # set from query data
        new_value = False

        if not edit_data:
            await Message.send_msg(chat_id, "I don't know which data to update! Please go back and then try again!")
            return

        try:
            await MongoDB.update_db(edit_cname, find_data, match_data, edit_data, new_value)
            await Message.send_msg(chat_id, f"Database updated!\n\nData: {edit_data}\nValue: <code>{new_value}</code>") 
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat_id, f"Error: {e}")

    elif data == "close":
        access = await _check_whois()
        if access:
            await query.message.delete()
