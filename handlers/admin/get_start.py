from utils.message_utils import text_editor
from aiogram import types, Dispatcher
from config.bot_data import admin_id, dp
from config.bot_text import text
from markups import cb
import markups as nav
from utils.revenue_send_all import send_all


@dp.message_handler(commands=['call_task'])
async def call_task(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer(text='Запуск отчетности')
        await send_all()