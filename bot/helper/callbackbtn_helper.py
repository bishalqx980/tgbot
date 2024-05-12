from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    data = query.data


    # youtube
    if data == "mp4":
        # importing from main.py
        from main import exe_func_ytdl
        url = context.user_data.get("url")
        extention = "mp4"
        await query.message.delete()
        await exe_func_ytdl(update, context, url, extention)

    elif data == "mp3":
        # importing from main.py
        from main import exe_func_ytdl
        url = context.user_data.get("url")
        extention = "mp3"
        await query.message.delete()
        await exe_func_ytdl(update, context, url, extention)
    
    # Group management
    elif data == "group_management":
        sent_msg = query.message

        msg = (
            "Group Moderation Commands -\n\n"
            "/tr » Translate any language\n"
            "/setlang » Set chat default language\n"
            "/echo » Make chat fun\n"
            "/id » Show chat/user id\n"
            "/welcome » To set welcome message in group\n"
            "/goodbye » To set goodbye message in group\n"
            "/antibot » Restrict other bots from joining in group\n"
            "/invite » Generate/Get invite link for Group\n"
            "/pin » Pin message loudly in group\n"
            "/unpin » Unpin a pinned message or all pinned messages\n"
            "/ban » Ban a member from group\n"
            "/unban » Unban a member from group\n"
            "/kick » Kick a member from group\n"
            "/kickme » The easy way to out\n"
            "/mute » Mute a member in group (member will be unable to send messages etc.)\n"
            "/unmute » Unmute a member (member will be able to send messages etc.)\n"
            "/lock » Lock the chat (no one can send messages etc.)\n"
            "/unlock » Unlock the chat (back to normal)\n"
            "/adminlist » See chat admins list\n"
            "/stats » Show chat config data\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "ai":
        sent_msg = query.message

        msg = (
            "Artificial Intelligent functions -\n\n"
            "/imagine » Generate AI image\n"
            "/gpt » Ask any question to ChatGPT\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "misc_func":
        sent_msg = query.message

        msg = (
            "Misc functions -\n\n"
            "/movie » Get any movie info by name/imdb_id\n"
            "/tr » Translate any language\n"
            "/setlang » Set chat default language\n"
            "/decode » Decode - base64 to text\n"
            "/encode » Encode - text to base64\n"
            "/shortener » Short any url\n"
            "/ping » Ping any url\n"
            "/calc » Calculate any math (supported syntex: +, -, *, /)\n"
            "/echo » Make chat fun\n"
            "/webshot » Take Screenshot of any website\n"
            "/weather » Get weather info of any city\n"
            "/ytdl » Download youtube video\n"
            "/yts » Search video on youtube\n"
            "/stats » Show chat config data\n"
            "/id » Show chat/user id\n\n"
            "<i>Note: Type commands to get more details about the command function!</i>"
        )

        btn_name = ["Back", "Close"]
        btn_data = ["help_menu", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.edit_msg(update, msg, sent_msg, btn)
    
    elif data == "owner_func":
        sent_msg = query.message

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
        sent_msg = query.message

        btn_name_row1 = ["Group Management", "AI"]
        btn_data_row1 = ["group_management", "ai"]

        btn_name_row2 = ["misc", "Bot owner"]
        btn_data_row2 = ["misc_func", "owner_func"]

        btn_name_row3 = ["Close"]
        btn_data_row3 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3)

        msg = (
            f"Hi! Welcome to the bot help section...\n"
            f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
            f"/start - to start the bot\n"
            f"/help - to see this message"
        )

        await Message.edit_msg(update, msg, sent_msg, row1 + row2 + row3)

    elif data == "unpin_all":
        # importing from group_management
        from bot.modules.group_management import exe_func_unpin_all_msg
        chat_id = context.chat_data.get("chat_id")
        await query.message.delete()
        await exe_func_unpin_all_msg(update, context, chat_id)
    
    # global close
    elif data == "close":
        await query.message.delete()
