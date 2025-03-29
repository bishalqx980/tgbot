from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB

async def query_chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("csettings_")

    # memory access
    data_center = MemoryDB.data_center.get(chat.id) # ChatID bcz its for both Private & Public Chat
    if not data_center:
        await query.answer("Session Expired.")
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(chat.id, [message_id, message_id - 1])
        except:
            pass
        return
    
    # verifying user
    user_id = data_center.get("user_id")
    if user_id != user.id:
        await query.answer("Access Denied!", True)
        return
    
    # common variable for chat_data and user_data
    memory_data = MemoryDB.chat_data.get(chat.id) or MemoryDB.user_data.get(chat.id)

    # variable required for global reply
    is_editing_btn = None
    is_boolean_btn = None

    if query_data == "menu":
        # Handling PRIVATE chat setting
        if chat.type == ChatType.PRIVATE:
            text = (
                "<blockquote><b>Chat Settings</b></blockquote>\n\n"

                f"• Name: {user.mention_html()}\n"
                f"• ID: <code>{user.id}</code>\n\n"

                f"• Language: <code>{memory_data.get('lang')}</code>\n"
                f"• Auto translate: <code>{memory_data.get('auto_tr') or False}</code>\n"
                f"• Echo: <code>{memory_data.get('echo') or False}</code>"
            )

            btn_data = [
                {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
                {"Echo": "csettings_echo", "Close": "csettings_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)
        
        else:
            pass
    
    elif query_data == "lang":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "lang",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Language: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> <a href='{}'>Available language codes</a>\nExample: <code>en</code> for English language.</blockquote>"
        ).format(memory_data.get("lang"), "https://telegra.ph/Language-Code-12-24")
    
    elif query_data == "auto_tr":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "auto_tr",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Auto translate: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will automatically translate chat messages to seleted language.</blockquote>"
        ).format(memory_data.get("auto_tr") or False)
    
    elif query_data == "echo":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "echo",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Echo: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will echo user messages.</blockquote>"
        ).format(memory_data.get("echo") or False)
    
    elif query_data == "welcome_user":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "welcome_user",
            "is_list": False,
            "is_int": False
        })

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Welcome Members: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will welcome new chat member, if enabled.</blockquote>"
        ).format(memory_data.get("welcome_user") or False)

        btn_data = [
            {"Enable": "database_bool_true", "Disable": "database_bool_false"},
            {"Custom Welcome Message": "csettings_custom_welcome_msg"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "custom_welcome_msg":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "custom_welcome_msg",
            "is_list": False,
            "is_int": False
        })

        custom_message = memory_data.get("custom_welcome_msg")

        if len(custom_message) > 500:
            await context.bot.send_message(chat.id, f"Custom Greeting Message:\n\n{custom_message}")
            custom_message = "Message is too long."
        
        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Custom Welcome Message:\n<code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Custom welcome message to greet new chat members. (supports telegram formatting)</blockquote>"
        ).format(custom_message)

        btn_data = [
            {"Set Custom Message": "database_edit_value", "Remove Custom Message": "database_rm_value"},
            {"Formattings": "csettings_formattings"},
            {"Back": "csettings_welcome_user", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "formattings":
        text = (
            "<blockquote><b>Formattings</b></blockquote>\n\n"
            "• <code>{first}</code> - users firstname\n"
            "• <code>{last}</code> - users lastname\n"
            "• <code>{fullname}</code> - users fullname\n"
            "• <code>{username}</code> - users username\n"
            "• <code>{mention}</code> - mention user\n"
            "• <code>{id}</code> - users ID\n"
            "• <code>{chatname}</code> - chat title"
        )

        btn = ButtonMaker.cbutton([{"Back": "csettings_custom_welcome_msg", "Close": "csettings_close"}])
    
    elif query_data == "farewell_user":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "farewell_user",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Farewell Members: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will send a farewell message to chat when a member left, if enabled.\n</blockquote>"
        ).format(memory_data.get("farewell_user"))
    
    elif query_data == "antibot":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "antibot",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Antibot: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> If someone try to add bots in chat, this will kick the bot, if enabled.</blockquote>"
        ).format(memory_data.get("antibot"))










        






























    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(user.id, [message_id, message_id - 1])
        except:
            pass
        return # don't want to edit message by global reply
    
    # common editing keyboard buttons
    if is_editing_btn:
        btn_data = [
            {"Edit Value": "database_edit_value"},
            {"Remove Value": "database_rm_value"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data) # cant use btn as common bcz maybe there are other btn
    
    if is_boolean_btn:
        btn_data = [
            {"Enable": "database_bool_true", "Disable": "database_bool_false"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data) # cant use btn as common bcz maybe there are other btn
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
        



























        
#         else:
#             text = """
# <blockquote><b>Chat Settings</b></blockquote>

# • Title: {}
# • ID: <code>{}</code>

# • Lang: <code>{}</code>
# • Auto tr: <code>{}</code>
# • Echo: <code>{}</code>
# • Antibot: <code>{}</code>
# • Welcome user: <code>{}</code>
# • Farewell user: <code>{}</code>
# • Links: <code>{}</code>
# • Allowed links: <code>{}</code>
# """


#                 title = find_chat.get("title")
#             lang = find_chat.get("lang")
#             echo = find_chat.get("echo", False)
#             auto_tr = find_chat.get("auto_tr", False)
#             welcome_user = find_chat.get("welcome_user", False)
#             farewell_user = find_chat.get("farewell_user", False)
#             antibot = find_chat.get("antibot", False)
#             is_links_allowed = find_chat.get("is_links_allowed")
#             allowed_links_list = find_chat.get("allowed_links_list")
            
#             if allowed_links_list:
#                 allowed_links_list = ", ".join(allowed_links_list)

#             text = chat_settings_menu_group.format(
#                 title,
#                 chat.id,
#                 lang,
#                 auto_tr,
#                 echo,
#                 antibot,
#                 welcome_user,
#                 farewell_user,
#                 is_links_allowed,
#                 allowed_links_list
#             )

#             btn_data = [
#                 {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
#                 {"Echo": "query_chat_set_echo", "Anti bot": "query_chat_antibot"},
#                 {"Welcome": "query_chat_welcome_user", "Farewell": "query_chat_farewell_user"},
#                 {"Links": "query_chat_links_behave", "Close": "query_close"}
#             ]

#             btn = ButtonMaker.cbutton(btn_data)
        
#         if effective_message.text:
#             await effective_message.edit_text(text, reply_markup=btn)
#         elif effective_message.caption:
#             await effective_message.edit_caption(text, reply_markup=btn)



