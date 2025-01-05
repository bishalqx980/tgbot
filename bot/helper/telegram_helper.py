from telegram import Update, ReactionTypeEmoji, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.error import Forbidden
from bot import bot, logger


class Message:
    async def send_msg(chat_id, msg, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=bool(True)):
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_message(
                chat_id=chat_id,
                text=msg,
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


    async def send_img(chat_id, img, caption=None, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML):
        """
        photo (:obj:`str` | :term:`file object` | :class:`~telegram.InputFile` | :obj:`bytes` \
            | :class:`pathlib.Path` | :class:`telegram.PhotoSize`): Photo to send.
            |fileinput|
            Lastly you can pass an existing :class:`telegram.PhotoSize` object to send.

            Caution:
                * The photo must be at most 10MB in size.
                * The photo's width and height must not exceed 10000 in total.
                * Width and height ratio must be at most 20.
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_photo(
                chat_id=chat_id,
                photo=img,
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


    async def send_vid(chat_id, video, thumbnail=None, caption=None, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML):
        """
        video (:obj:`str` | :term:`file object` | :class:`~telegram.InputFile` | :obj:`bytes` \
            | :class:`pathlib.Path` | :class:`telegram.Video`): Video file to send.
            |fileinput|
            Lastly you can pass an existing :class:`telegram.Video` object to send.
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


    async def send_audio(chat_id, audio, title, caption=None, btn=None, reply_message_id=None, parse_mode=ParseMode.HTML):
        """
        audio (:obj:`str` | :term:`file object` | :class:`~telegram.InputFile` | \
            :obj:`bytes` | :class:`pathlib.Path` | :class:`telegram.Audio`): Audio file to
            send. |fileinput|
            Lastly you can pass an existing :class:`telegram.Audio` object to send.
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


    async def send_doc(chat_id, doc, filename, caption=None, btn=None, reply_message_id=None, parse_mode=ParseMode.HTML):
        """
        document (:obj:`str` | :term:`file object` | :class:`~telegram.InputFile` | \
        :obj:`bytes` | :class:`pathlib.Path` | :class:`telegram.Document`): File to send.
        |fileinput|
        Lastly you can pass an existing :class:`telegram.Document` object to send.

        Note:
            Sending by URL will currently only work ``GIF``, ``PDF`` & ``ZIP`` files.
        """
        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await bot.send_document(
                chat_id=chat_id,
                document=doc,
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


    async def reply_msg(update: Update, msg, reply_message_id=None, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=bool(True)):
        """
        `reply_message_id` default value is `effective message` or `replied message`
        """
        e_msg = update.effective_message
        msg_id = reply_message_id or (e_msg.reply_to_message.message_id if e_msg.reply_to_message else e_msg.message_id)

        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        try:
            response = await update.message.reply_text(
                text=msg,
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


    async def forward_msg(to_chat_id, from_chat_id, message_id):
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


    async def edit_msg(update: Update, new_text, message_to_edit, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=bool(True)):
        """
        `message_to_edit` could be the `ref message` or `ref message id`
        """
        is_caption = message_to_edit.caption
        chat_id = update.effective_chat.id
        msg_id = message_to_edit.message_id or message_to_edit

        reply_markup = InlineKeyboardMarkup(btn) if btn else None

        if is_caption:
            try:
                response = await bot.edit_message_caption(
                    caption=new_text,
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
                    text=new_text,
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


    async def del_msg(chat_id, message_to_delete):
        msg_id = message_to_delete.message_id or message_to_delete

        try:
            response = await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    async def del_msgs(chat_id, message_to_delete_id_list=list):
        try:
            response = await bot.delete_messages(chat_id=chat_id, message_ids=message_to_delete_id_list)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    async def react_msg(chat_id, message_id, reaction=str("❤"), is_big=bool(True)):
        """
        Example: reaction = "👍"\n
        Reaction emoji. Currently, it can be one of "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"
        """
        try:
            response = await bot.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(reaction)], is_big)
            return response
        except Exception as e:
            logger.error(e)


class Button:
    async def ubutton(data, same_line=bool(False)):
        """
        URL ButtonMaker\n
        Example usage:\n
        btn_data = {\n
            "btn_name": "btn_url",\n
            "btn_name_2": "btn_url_2"\n
        }\n
        row1 = await Button.ubutton(btn_data, True) # 1st line and both button are in same line\n
        btn = row1\n
        """
        btn, sbtn = [], []
        try:
            for b_name, b_url in data.items():
                if same_line and len(data) > 1:
                    sbtn.append(InlineKeyboardButton(b_name, b_url))
                else:
                    btn.append([InlineKeyboardButton(b_name, b_url)])
            buttons = btn + [sbtn]
            return buttons
        except Exception as e:
            logger.error(e)


    async def cbutton(data, same_line=bool(False)):
        """
        Callback ButtonMaker\n
        Example usage:\n
        btn_data = {\n
            "btn_name": "btn_data",\n
            "btn_name_2": "btn_data_2"\n
        }\n
        row1 = await Button.cbutton(btn_data, True) # 1st line and both button are in same line\n
        btn = row1\n
        """
        btn, sbtn = [], []
        try:
            for b_name, b_data in data.items():
                if same_line and len(data) > 1:
                    sbtn.append(InlineKeyboardButton(b_name, callback_data=b_data))
                else:
                    btn.append([InlineKeyboardButton(b_name, callback_data=b_data)])
            buttons = btn + [sbtn]
            return buttons
        except Exception as e:
            logger.error(e)
