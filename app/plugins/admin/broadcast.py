import asyncio
from time import time
from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import Forbidden

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import sudo_required, privatechat_only
from app.database import MongoDB
from app.modules.utils import UTILITY


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "broadcast",
    "commands": ["broadcast", "bcast"], # list of commands including aliases

    "description": "Broadcast message to bot users!",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Broadcast", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


class BROADCAST_DATA:
    BROADCAST_LIST = set()
    CANCEL_BROADCAST = False

    MENU_TEXT = (
        "> Broadcast Menu\n\n"
        "🖼️ Media: {b_media}\n"
        "💬 Message: {b_message}\n"
        # "📦 Buttons: {b_buttons}\n\n"
        "<i>Note: Set everything then click on view final message. If everything is ok then broadcast the message. (media & message both can't be none at once)</i>"
    )

    MENU_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🖼️ Set Media", "broadcast:set_value"),
            InlineKeyboardButton("🧹 Remove Media", "broadcast:remove:b_media")
        ],
        [
            InlineKeyboardButton("💬 Set Message", "broadcast:set_value"),
            InlineKeyboardButton("🧹 Remove Message", "broadcast:remove:b_message")
        ],
        # [
        #     InlineKeyboardButton("📦 Set Buttons", "broadcast:set_value"),
        #     InlineKeyboardButton("🧹 Remove Buttons", "broadcast:remove:b_buttons")
        # ],
        [
            InlineKeyboardButton("👀 View Final Message", "broadcast:output"),
            InlineKeyboardButton("✘ Cancel", "broadcast:cancel")
        ]
    ])

    B_PHOTO = None
    B_VIDEO = None
    B_MESSAGE = None
    B_BUTTONS = None


def broadcast_filter(_, __, message:Message):
    user = message.from_user or message.sender_chat
    return user and user.id in BROADCAST_DATA.BROADCAST_LIST

is_broadcasting = filters.create(broadcast_filter)


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@sudo_required
async def func_(_, message: Message):
    await message.reply(
        BROADCAST_DATA.MENU_TEXT.format(
            b_media = "Set" if BROADCAST_DATA.B_PHOTO or BROADCAST_DATA.B_VIDEO else "Not Set",
            b_message = "Set" if BROADCAST_DATA.B_MESSAGE else "Not Set",
            b_buttons = "Set" if BROADCAST_DATA.B_BUTTONS else "Not Set",
        ),
        reply_markup=BROADCAST_DATA.MENU_BUTTONS
    )


async def start_broadcast(message: Message):
    sent_message = await message.reply(
        "Starting broadcast..."
    )

    # Getting active user ids
    user_ids = MongoDB.get_field_values(
        MongoDB.USERS,
        "user_id"
    )

    active_status = MongoDB.get_field_values(
        MongoDB.USERS,
        "active_status"
    )

    active_users = []

    if len(user_ids) != len(active_status):
        active_users = user_ids
    
    else:
        combined_list = list(zip(user_ids, active_status))
        for uid, is_active in combined_list:
            if is_active:
                active_users.append(uid)

    # Broadcast message elements
    B_PHOTO = BROADCAST_DATA.B_PHOTO
    B_VIDEO = BROADCAST_DATA.B_VIDEO
    B_MESSAGE = BROADCAST_DATA.B_MESSAGE
    B_BUTTONS = BROADCAST_DATA.B_BUTTONS
    # callback broadcast:cancel is used for multiple task so we need to make sure cancel is false
    BROADCAST_DATA.CANCEL_BROADCAST = False

    succeed = []
    failed = []

    broadcastStartTime = time()

    for uid in active_users:

        if BROADCAST_DATA.CANCEL_BROADCAST:
            await message.reply(
                "\n\n> Broadcast has been canceled by user!"
            )
            break

        try:

            if BROADCAST_DATA.B_PHOTO:
                await bot.send_photo(
                    uid,
                    B_PHOTO,
                    caption=B_MESSAGE,
                    reply_markup=B_BUTTONS
                )

            elif BROADCAST_DATA.B_VIDEO:
                await bot.send_video(
                    uid,
                    B_VIDEO,
                    caption=B_MESSAGE,
                    reply_markup=B_BUTTONS
                )
            
            else:
                await bot.send_message(
                    uid,
                    B_MESSAGE,
                    reply_markup=B_BUTTONS
                )

            succeed.append(uid)

        except Forbidden:
            failed.append(f"Forbidden: {uid}")
            # updating MongoDB
            MongoDB.update(
                MongoDB.USERS,
                "user_id",
                uid,
                { "active_status": False }
            )
        
        except Exception as e:
            failed.append(f"{e}: {uid}")

        try:

            percent = (len(succeed) + len(failed)) * 100 / len(active_users)
            progress_bar = UTILITY.createProgressBar(percent)

            sent_message = await sent_message.edit_text(
                "> **Broadcast**\n\n"

                "**📦 Database information**\n"
                f"**• Total users:** `{len(user_ids)}`\n"
                f"**• Active users:** `{len(active_users)}`\n\n"

                "**📊 Progress**\n"
                f"**• Sent:** `{len(succeed)}`\n"
                f"**• Exception:** `{len(failed)}`\n"
                f"**• Progress:** `{percent:.2f}%`\n"
                f"{progress_bar}", # progress bar
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✘ Cancel", "broadcast:cancel")
                ]])
            )

        except Exception as e:
            logger.error(e)

        await asyncio.sleep(0.5)

    # End of the broadcast : result
    broadcastEndTime = time()

    if (broadcastEndTime - broadcastStartTime) > 60:
        time_taken = f"{((broadcastEndTime - broadcastStartTime) / 60):.2f} min"
    
    else:
        time_taken = f"{(broadcastEndTime - broadcastStartTime):.2f} sec"
    
    await sent_message.edit_text(
        sent_message.html_text + f"\n\n> Broadcast Done! Time taken : {time_taken}"
    )

    if failed:
        failed_file = BytesIO(", ".join(failed).encode())
        failed_file.name = "failed.txt"

        await message.reply_document(
            failed_file,
            caption=f"Total failed: {len(failed)}"
        )


@bot.on_callback_query(filters.regex(r"^broadcast:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    query_data = query.data.removeprefix("broadcast:")
    user_id = query.from_user.id

    if query_data == "menu":
        return await query.edit_message_text(
            BROADCAST_DATA.MENU_TEXT.format(
                b_media = "Set" if BROADCAST_DATA.B_PHOTO or BROADCAST_DATA.B_VIDEO else "Not Set",
                b_message = "Set" if BROADCAST_DATA.B_MESSAGE else "Not Set",
                b_buttons = "Set" if BROADCAST_DATA.B_BUTTONS else "Not Set",
            ),
            reply_markup=BROADCAST_DATA.MENU_BUTTONS
        )

    elif query_data == "start":
        await query.message.delete()
        await query.answer("Broadcast started!")
        await start_broadcast(query.message)

    elif query_data == "output":
        B_PHOTO = BROADCAST_DATA.B_PHOTO
        B_VIDEO = BROADCAST_DATA.B_VIDEO
        B_MESSAGE = BROADCAST_DATA.B_MESSAGE
        B_BUTTONS = BROADCAST_DATA.B_BUTTONS

        if not B_MESSAGE and not (B_PHOTO and B_VIDEO):
            return await query.answer(
                "⚠️ Media & Message both can't be none at once.",
                True
            )

        await query.answer()

        if BROADCAST_DATA.B_PHOTO:
            try:

                await query.message.reply_photo(
                    B_PHOTO,
                    caption=B_MESSAGE,
                    reply_markup=B_BUTTONS
                )

            except Exception as e:
                await query.message.reply_text(
                    f"Error: {e}"
                )

        elif BROADCAST_DATA.B_VIDEO:
            try:

                await query.message.reply_video(
                    B_VIDEO,
                    caption=B_MESSAGE,
                    reply_markup=B_BUTTONS
                )

            except Exception as e:
                await query.message.reply_text(
                    f"Error: {e}"
                )

        else:
            try:

                await query.message.reply(
                    B_MESSAGE,
                    reply_markup=B_BUTTONS
                )

            except Exception as e:
                await query.message.reply_text(
                    f"Error: {e}"
                )

        await query.message.reply(
            "Start broadcast?",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("☰ Menu", "broadcast:menu"),
                InlineKeyboardButton("📡 Start", "broadcast:start")
            ]])
        )

    elif query_data == "set_value":
        # for custom filter
        BROADCAST_DATA.BROADCAST_LIST.add(user_id)

        return await query.edit_message_text(
            (
                "Waiting for data...\n\n"
                "Media : Photo / Video\n"
                "Message : markdown format supported\n"
                "Message & Buttons [formatting]()"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("☰ Menu", "broadcast:menu")
            ]])
        )

    elif query_data.startswith("remove:"):
            data = query_data.removeprefix("remove:")

            if data == "b_media":
                BROADCAST_DATA.B_PHOTO = None
                BROADCAST_DATA.B_VIDEO = None
    
            elif data == "b_message":
                BROADCAST_DATA.B_MESSAGE = None
    
            elif data == "b_buttons":
                BROADCAST_DATA.B_BUTTONS = None

            await query.answer("✅ Successful!", True)

            try:
                
                await query.edit_message_text(
                    BROADCAST_DATA.MENU_TEXT.format(
                        b_media = "Set" if BROADCAST_DATA.B_PHOTO or BROADCAST_DATA.B_VIDEO else "Not Set",
                        b_message = "Set" if BROADCAST_DATA.B_MESSAGE else "Not Set",
                        b_buttons = "Set" if BROADCAST_DATA.B_BUTTONS else "Not Set",
                    ),
                    reply_markup=BROADCAST_DATA.MENU_BUTTONS
                )

            except Exception as e:
                logger.error(e)
            return

    elif query_data == "cancel":
        
        BROADCAST_DATA.BROADCAST_LIST.discard(user_id)
        BROADCAST_DATA.CANCEL_BROADCAST = True

        return await query.edit_message_text(
            "Broadcast canceled!"
        )


@bot.on_message((filters.text | filters.video | filters.photo) & is_broadcasting)
async def func_(_, message: Message):
    BROADCAST_DATA.BROADCAST_LIST.discard(message.from_user.id)

    if message.photo:
        BROADCAST_DATA.B_PHOTO = message.photo.file_id

    if message.video: 
        BROADCAST_DATA.B_VIDEO = message.video.file_id

    if message.text or message.caption:
        if message.text:
            BROADCAST_DATA.B_MESSAGE = message.text.html

        elif message.caption:
            BROADCAST_DATA.B_MESSAGE = message.caption.html

    await message.reply(
        BROADCAST_DATA.MENU_TEXT.format(
            b_media = "Set" if BROADCAST_DATA.B_PHOTO or BROADCAST_DATA.B_VIDEO else "Not Set",
            b_message = "Set" if BROADCAST_DATA.B_MESSAGE else "Not Set",
            b_buttons = "Set" if BROADCAST_DATA.B_BUTTONS else "Not Set",
        ),
        reply_markup=BROADCAST_DATA.MENU_BUTTONS
    )
