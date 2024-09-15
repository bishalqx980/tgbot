from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.error import Forbidden
from bot import bot, logger

class Message:
    async def send_msg(chat_id, msg, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    reply_markup=reply_markup,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        else:
            try:
                response = await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)


    async def send_img(chat_id, img, caption=None, btn=None, parse_mode=ParseMode.HTML):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_photo(
                    chat_id=chat_id,
                    photo=img,
                    caption=caption,
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
                response = await bot.send_photo(
                    chat_id=chat_id,
                    photo=img,
                    caption=caption,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)


    async def send_vid(chat_id, video, thumbnail=None, caption=None, reply_msg_id=None, btn=None, parse_mode=ParseMode.HTML):
        if btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.send_video(
                    chat_id=chat_id,
                    video=video,
                    caption=caption,
                    reply_to_message_id=reply_msg_id,
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
        else:
            try:
                response = await bot.send_video(
                    chat_id=chat_id,
                    video=video,
                    caption=caption,
                    reply_to_message_id=reply_msg_id,
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


    async def send_audio(chat_id, audio, title, caption=None, reply_msg_id=None, parse_mode=ParseMode.HTML):
        try:
            response = await bot.send_audio(
                chat_id=chat_id,
                audio=audio,
                title=title,
                caption=caption,
                reply_to_message_id=reply_msg_id,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    async def send_doc(chat_id, doc, filename, caption=None, reply_msg_id=None, parse_mode=ParseMode.HTML):
        """
        doc = send as file > open()
        """
        try:
            response = await bot.send_document(
                chat_id=chat_id,
                document=doc,
                filename=filename,
                caption=caption,
                reply_to_message_id=reply_msg_id,
                parse_mode=parse_mode
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    async def reply_msg(update: Update, msg, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        chat = update.effective_chat
        e_msg = update.effective_message
        re_msg = e_msg.reply_to_message
        msg_id = re_msg.message_id if re_msg else e_msg.message_id

        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            try:
                response = await update.message.reply_text(
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    reply_to_message_id=msg_id,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
                try:
                    reply_markup = InlineKeyboardMarkup(btn)
                    response = await bot.send_message(
                        chat_id=chat.id,
                        text=msg,
                        reply_markup=reply_markup,
                        disable_web_page_preview=bool(disable_web_preview),
                        parse_mode=parse_mode
                    )
                    return response
                except Forbidden:
                    return Forbidden
                except Exception as e:
                    logger.error(e)
        else:
            try:
                response = await update.message.reply_text(
                    text=msg,
                    disable_web_page_preview=bool(disable_web_preview),
                    reply_to_message_id=msg_id,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
                try:
                    response = await bot.send_message(
                        chat_id=chat.id,
                        text=msg,
                        disable_web_page_preview=bool(disable_web_preview),
                        parse_mode=parse_mode
                    )
                    return response
                except Forbidden:
                    return Forbidden
                except Exception as e:
                    logger.error(e)


    async def forward_msg(chat_id, from_chat_id, msg_id):
        """
        chat_id > where you want to send\n
        from_chat_id > effective chat id\n
        msg_id > effective message id
        """
        try:
            response = await bot.forward_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=msg_id
            )
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


    async def edit_msg(update: Update, edit_msg_text, sent_msg_pointer, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        caption_msg = sent_msg_pointer.caption
        chat_id = update.effective_chat.id
        msg_id = sent_msg_pointer.message_id

        if caption_msg and btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.edit_message_caption(
                    caption=edit_msg_text,
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
        elif caption_msg and not btn:
            try:
                response = await bot.edit_message_caption(
                    caption=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        elif not caption_msg and btn:
            try:
                reply_markup = InlineKeyboardMarkup(btn)
                response = await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)
        elif not caption_msg and not btn:
            try:
                response = await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
                return response
            except Forbidden:
                return Forbidden
            except Exception as e:
                logger.error(e)


    async def del_msg(chat_id, msg_pointer=None, msg_id=None):
        if not msg_pointer and not msg_id:
            logger.error("msg_pointer or msg_id not specified!")
            return
        
        msg_id = msg_pointer.message_id if msg_pointer else msg_id
        try:
            response = await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            return response
        except Forbidden:
            return Forbidden
        except Exception as e:
            logger.error(e)


class Button:
    async def ubutton(data, same_line=bool(False)):
        """
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
