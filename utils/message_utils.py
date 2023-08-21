from aiogram.utils.exceptions import BadRequest
from config.bot_data import admin_id
from config.bot_data import bot
from aiogram import types
import asyncio


async def text_editor(text: str, call: types.CallbackQuery = None, markup=None, message: types.Message = None,
                      message_id: types.MessageId = None, user_id: int = None) -> types.Message:
    chat_id = call.from_user.id if call else message.from_user.id
    message_id = message_id if message_id else (call.message.message_id if call else message.message_id)
    try:
        msg = await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup,
                                          disable_web_page_preview=True)
    except BadRequest:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            await bot.delete_message(chat_id=chat_id, message_id=message_id - 1)
        except BadRequest:
            pass
        msg = await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, disable_web_page_preview=True)
    return msg


async def admin_send_message(text: str):
    async def admin_sender(text: str):
        for ID in admin_id:
            try:
                await bot.send_message(ID, text)
            except:
                pass

    asyncio.create_task(admin_sender(text))
