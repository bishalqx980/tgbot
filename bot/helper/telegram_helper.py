from telegram import Update, ReactionTypeEmoji, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.error import Forbidden
from bot import bot, logger


class Message:
    @staticmethod
    async def send_message(chat_id, message, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_to_message_id=reply_message_id,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_preview,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def send_image(chat_id, image, caption=None, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML):
        """
        `image` type: `file object` | `url`
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_photo(
                chat_id=chat_id,
                photo=image,
                caption=caption,
                reply_to_message_id=reply_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def send_video(chat_id, video, thumbnail=None, caption=None, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML):
        """
        `video` type: `file object` | `url`
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                reply_to_message_id=reply_message_id,
                reply_markup=reply_markup,
                thumbnail=thumbnail,
                height=1080,
                width=1920,
                supports_streaming=True,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def send_audio(chat_id, audio, title, caption=None, btn=None, reply_message_id=None, parse_mode=ParseMode.HTML):
        """
        `audio` type: `file object` | `url`
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_audio(
                chat_id=chat_id,
                audio=audio,
                title=title,
                caption=caption,
                reply_markup=reply_markup,
                reply_to_message_id=reply_message_id,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def send_document(chat_id, document, filename, caption=None, btn=None, reply_message_id=None, parse_mode=ParseMode.HTML):
        """
        `document` type: `file object` | `url`
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_document(
                chat_id=chat_id,
                document=document,
                filename=filename,
                caption=caption,
                reply_markup=reply_markup,
                reply_to_message_id=reply_message_id,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def reply_message(update: Update, message, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        """
        `reply_message_id` default value is `effective message` or `replied message`
        """
        e_msg = update.effective_message
        msg_id = reply_message_id or (e_msg.reply_to_message.message_id if e_msg.reply_to_message else e_msg.message_id)

        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await update.message.reply_text(
                text=message,
                disable_web_page_preview=disable_web_preview,
                reply_to_message_id=msg_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def reply_image(update: Update, image, caption=None, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML):
        """
        `reply_message_id` default value is `effective message` or `replied message`
        """
        e_msg = update.effective_message
        msg_id = reply_message_id or (e_msg.reply_to_message.message_id if e_msg.reply_to_message else e_msg.message_id)

        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await update.message.reply_photo(
                photo=image,
                caption=caption,
                reply_to_message_id=msg_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def forward_message(to_chat_id, from_chat_id, message_id):
        try:
            response = await bot.forward_message(
                chat_id=to_chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def edit_message(update: Update, new_message, message_to_edit, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        """
        `message_to_edit` could be the `ref message` or `ref message id`
        """
        is_caption = message_to_edit.caption
        chat_id = update.effective_chat.id
        msg_id = getattr(message_to_edit, "message_id", message_to_edit)

        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        if is_caption:
            try:
                response = await bot.edit_message_caption(
                    caption=new_message,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        else:
            try:
                response = await bot.edit_message_text(
                    text=new_message,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_web_preview,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)


    @staticmethod
    async def delete_message(chat_id, message_to_delete):
        """
        `message_to_delete` could be the `ref message` or `ref message id`
        """
        msg_id = getattr(message_to_delete, "message_id", message_to_delete)

        try:
            response = await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def delete_messages(chat_id, message_id_list=list):
        try:
            response = await bot.delete_messages(chat_id=chat_id, message_ids=message_id_list)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def react_message(chat_id, message_id, reaction="❤", is_big=True):
        """
        Reaction emoji. Currently, it can be one of "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"
        """
        try:
            response = await bot.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(reaction)], is_big)
            return response
        except Exception as e:
            logger.error(e)


class Button:
    @staticmethod
    async def ubutton(data, same_line=False):
        """
        _url button maker_\n
        `data` type: dict | `same_line` boolean\n
        returns `list` | `None`
        """
        try:
            buttons = [
                InlineKeyboardButton(btn_name, btn_url) for btn_name, btn_url in data.items()
            ]

            if same_line and len(data) > 1:
                return [buttons]
            else:
                return [[button] for button in buttons]
        except Exception as e:
            logger.error(e)


    @staticmethod
    async def cbutton(data, same_line=False):
        """
        _callback button maker_\n
        `data` type: dict | `same_line` boolean\n
        returns `list` | `None`
        """
        try:
            buttons = [
                InlineKeyboardButton(btn_name, callback_data=btn_data) for btn_name, btn_data in data.items()
            ]

            if same_line and len(data) > 1:
                return [buttons]
            else:
                return [[button] for button in buttons]
        except Exception as e:
            logger.error(e)
