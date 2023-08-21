import datetime
import json

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from config.bot_data import db, money_name, bot_username, dp, bot
from config.settings_res import *
from states.states import Product
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text
from config.bot_text import Text
from markups import cb
import markups as nav
from config.bot_text import Text


@dp.callback_query_handler(lambda x: x.data == 'otziv')
async def get_otziv(callback: types.CallbackQuery):
    result = await db.read_review(user_id=callback.from_user.id)
    if result == None:
        await bot.answer_callback_query(text=text.no_review, callback_query_id=callback.id, show_alert=True)
        return
    result_dict = json.loads(result)
    spisok = []
    for item in result_dict:
        try:
            texts = result_dict.get(str(item))
            spisok.append(texts)
        except:
            continue

    count = 0
    text_send = ""
    for i in spisok:
        count += 1
        text_send += f'{count}. <i>{i}</i>\n'

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action='profile')))
    await text_editor(call=callback,
                      text=text.review_send + text_send,
                      markup=markup)


@dp.callback_query_handler(lambda x: x.data == 'jalob')
async def get_otziv(callback: types.CallbackQuery):
    result = await db.cheack_otziv_conflict(user_id=callback.from_user.id)
    if result == None:
        await bot.answer_callback_query(text=text.no_conflict, callback_query_id=callback.id, show_alert=True)
        return

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action='profile')))
    await text_editor(call=callback,
                      text=text.review_send_conflict.format(count_conflict=result[1],
                                                            money_conflict=result[0]),
                      markup=markup)


@dp.callback_query_handler(lambda x: x.data == 'settings_citchen')
async def change_set(callback: types.CallbackQuery):
    citc1, citc2, citc3, date = await db.cheack_cithcen_work(user_id=callback.from_user.id)
    work = 'Работает'
    no_work = 'Не работает'
    await text_editor(text=text.settings_citchen.format(status1=work if citc1 == 0 else no_work,
                                                        status2=work if citc1 == 0 else no_work,
                                                        status3=work if citc1 == 0 else no_work),
                      markup=await nav.get_status(citc1, citc2, citc3), call=callback)


@dp.callback_query_handler(lambda x: x.data in ('change_conditer', 'change_barmen', 'change_chef'))
async def confirm(callback: types.CallbackQuery, state: FSMContext):
    day = datetime.date.today().strftime("%Y-%m-%d")
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    citc1, citc2, citc3, date = await db.cheack_cithcen_work(user_id=callback.from_user.id)
    if date == day:
        await bot.answer_callback_query(text=text.no_change_citchen.format(day=tomorrow_str), callback_query_id=callback.id, show_alert=True)
        return
    call = callback.data.split('_')
    await state.update_data(change=call[1])
    await text_editor(text=text.confirm_citchen, call=callback, markup=nav.confirm_citchen)


@dp.callback_query_handler(lambda x: x.data == 'confirmcitchen')
async def yes_change(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    get = data.get('change')
    citc1, citc2, citc3, date = await db.cheack_cithcen_work(user_id=callback.from_user.id)
    citc1 = 0 if citc1 == 1 else 1
    citc2 = 0 if citc2 == 1 else 1
    citc3 = 0 if citc3 == 1 else 1
    await db.change_citchen(user_id=callback.from_user.id, who=get, number=[citc1, citc2, citc3])
    citc1, citc2, citc3, date = await db.cheack_cithcen_work(user_id=callback.from_user.id)
    work = 'Работает'
    no_work = 'Не работает'
    await text_editor(text=text.settings_citchen.format(status1=work if citc1 == 0 else no_work,
                                                        status2=work if citc1 == 0 else no_work,
                                                        status3=work if citc1 == 0 else no_work),
                      markup=await nav.get_status(citc1, citc2, citc3), call=callback)
