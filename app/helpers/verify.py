import asyncio
from time import time

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot
from app.database import SessionData


async def verify_anonymous_admin(message: Message, timeout: int = 10):
    """
    Anonymous admin verification
    """

    user = message.from_user or message.sender_chat

    chat_data = SessionData.get(message.chat.id, {})
    admin_data = chat_data.get("admin")
    cache_timout = 5

    # If we have cached anonymous admin data
    if admin_data:
        expire_time = admin_data.get("expire")

        # Cached data expired
        if expire_time and (time() - expire_time) > cache_timout:
            admin_data = None

    # No cached data or expired data
    if not admin_data:

        SessionData.insert(
            message.chat.id,
            {
                "admin": {
                    "user": None,
                    "expire": None # expire time will be added after verification
                }
            }
        )
    
        sent_message = await message.reply_text(
            f"UwU >.< , An annoymous admin! Click to verify yourself.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Verify", "verify:anonymous_admin")
            ]])
        )
    
        for i in range(timeout):
            chat_data = SessionData.get(message.chat.id)
            admin_data = chat_data.get("admin")
            user = admin_data.get("user")
    
            if user:
                break
            
            await asyncio.sleep(1)
    
        await sent_message.delete()
    
        if not user:
            try:
                await message.delete()
            except:
                pass

            return await message.reply_text(
                "(timeout/other) Unable to verify. Please try again."
            )
    
    return admin_data.get("user")


@bot.on_callback_query(filters.regex(r"^verify:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    if query.data == "verify:anonymous_admin":
        SessionData.insert(
            query.message.chat.id,
            {
                "admin": {
                    "user": query.from_user,
                    "expire": time()
                }
            }
        )

        await query.answer("✅ Verified.", True)
