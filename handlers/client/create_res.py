from aiogram.dispatcher import FSMContext

from config.bot_data import db, money_name, bot_username, dp, bot
from config.settings_res import *
from states.states import Client
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav
from config.bot_text import Text


@dp.message_handler(state=Client.Create_res.name)
async def create(message: types.Message, state: FSMContext):
    try:
        await db.add_client(user_id=message.from_user.id, username=message.from_user.username)
        await db.create_res(user_id=message.from_user.id, name=message.text)
        await text_editor(text=text.main_menu.format(money_name=money_name),
                          message=message,
                          markup=nav.main_menu(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()