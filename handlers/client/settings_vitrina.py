import asyncio
import json

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import itertools
from config.bot_data import db, money_name, bot_username, dp, bot
from states.states import Client
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import Text as GetText, text
from markups import cb
import markups as nav


# -----------------Решил не усложнять)---------------------
from utils.reporting import cheac_review


@dp.callback_query_handler(lambda x: x.data == 'settings_vitrina')
async def name_vitrina(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup()





    m1 = InlineKeyboardButton(text=text.name_vitrina1.format(wai='🔽'), callback_data='tricks')
    m2 = InlineKeyboardButton(text=text.name_vitrina2.format(wai='🔽'), callback_data='pricing')
    m3 = InlineKeyboardButton(text=text.name_vitrina3.format(wai='🔽'), callback_data='convenience')
    m4 = InlineKeyboardButton(text=text.name_vitrina4.format(wai='🔽'), callback_data='beauty')
    back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
    markup.add(m1).add(m2).add(m3).add(m4).add(back)
    await text_editor(text=GetText.desc_all_vitrina,
                      markup=markup,
                      call=callback)


@dp.callback_query_handler(lambda c: c.data in ['tricks', 'pricing', 'convenience', 'beauty'])
async def show_additional_buttons(callback_query: types.CallbackQuery, category: str = None):
    if category is None:
        category = callback_query.data

    good = await db.cheack_sett(user_id=callback_query.from_user.id)
    if category == 'tricks':
        get = GetText.desc_vitrina_1
        markup = InlineKeyboardMarkup()
        m1 = InlineKeyboardButton(text=text.name_vitrina1.format(wai='🔼'), callback_data='settings_vitrina')
        m5 = InlineKeyboardButton(text=text.dop_vitrina1_1.format(cheack=good[2]), callback_data='additional_3_1_tricks')
        m6 = InlineKeyboardButton(text=text.dop_vitrina1_2.format(cheack=good[1]), callback_data='additional_2_1_tricks')
        m7 = InlineKeyboardButton(text=text.dop_vitrina1_3.format(cheack=good[0]), callback_data='additional_1_1_tricks')
        m2 = InlineKeyboardButton(text=text.name_vitrina2.format(wai='🔽'), callback_data='pricing')
        m3 = InlineKeyboardButton(text=text.name_vitrina3.format(wai='🔽'), callback_data='convenience')
        m4 = InlineKeyboardButton(text=text.name_vitrina4.format(wai='🔽'), callback_data='beauty')
        back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
        markup.add(m1).add(m5, m6).add(m7).add(m2).add(m3).add(m4).add(back)
    elif category == 'pricing':
        get = GetText.desc_vitrina_2
        markup = InlineKeyboardMarkup()
        m1 = InlineKeyboardButton(text=text.name_vitrina1.format(wai='🔽'), callback_data='tricks')
        m5 = InlineKeyboardButton(text=text.dop_vitrina2_1.format(cheack=good[5]), callback_data='additional_3_2_pricing')
        m6 = InlineKeyboardButton(text=text.dop_vitrina2_2.format(cheack=good[4]), callback_data='additional_2_2_pricing')
        m7 = InlineKeyboardButton(text=text.dop_vitrina2_3.format(cheack=good[3]), callback_data='additional_1_2_pricing')
        m2 = InlineKeyboardButton(text=text.name_vitrina2.format(wai='🔼'), callback_data='settings_vitrina')
        m3 = InlineKeyboardButton(text=text.name_vitrina3.format(wai='🔽'), callback_data='convenience')
        m4 = InlineKeyboardButton(text=text.name_vitrina4.format(wai='🔽'), callback_data='beauty')
        back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
        markup.add(m1).add(m2).add(m5, m6).add(m7).add(m3).add(m4).add(back)
    elif category == 'convenience':
        get = GetText.desc_vitrina_3
        markup = InlineKeyboardMarkup()
        m1 = InlineKeyboardButton(text=text.name_vitrina1.format(wai='🔽'), callback_data='tricks')
        m5 = InlineKeyboardButton(text=text.dop_vitrina3_1.format(cheack=good[9]), callback_data='additional_4_3_convenience')
        m6 = InlineKeyboardButton(text=text.dop_vitrina3_2.format(cheack=good[8]), callback_data='additional_3_3_convenience')
        m7 = InlineKeyboardButton(text=text.dop_vitrina3_3.format(cheack=good[7]), callback_data='additional_2_3_convenience')
        m8 = InlineKeyboardButton(text=text.dop_vitrina3_4.format(cheack=good[6]), callback_data='additional_1_3_convenience')
        m2 = InlineKeyboardButton(text=text.name_vitrina2.format(wai='🔽'), callback_data='pricing')
        m3 = InlineKeyboardButton(text=text.name_vitrina3.format(wai='🔼'), callback_data='settings_vitrina')
        m4 = InlineKeyboardButton(text=text.name_vitrina4.format(wai='🔽'), callback_data='beauty')
        back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
        markup.add(m1).add(m2).add(m3).add(m5, m6).add(m7, m8).add(m4).add(back)
    elif category == 'beauty':
        get = GetText.desc_vitrina_4
        markup = InlineKeyboardMarkup()

        m1 = InlineKeyboardButton(text=text.name_vitrina1.format(wai='🔽'), callback_data='tricks')
        m5 = InlineKeyboardButton(text=text.dop_vitrina4_1.format(cheack=good[13]), callback_data='additional_4_4_beauty')
        m6 = InlineKeyboardButton(text=text.dop_vitrina4_2.format(cheack=good[12]), callback_data='additional_3_4_beauty')
        m7 = InlineKeyboardButton(text=text.dop_vitrina4_3.format(cheack=good[11]), callback_data='additional_2_4_beauty')
        m8 = InlineKeyboardButton(text=text.dop_vitrina4_4.format(cheack=good[10]), callback_data='additional_1_4_beauty')
        m2 = InlineKeyboardButton(text=text.name_vitrina2.format(wai='🔽'), callback_data='pricing')
        m3 = InlineKeyboardButton(text=text.name_vitrina3.format(wai='🔽'), callback_data='convenience')
        m4 = InlineKeyboardButton(text=text.name_vitrina4.format(wai='🔼'), callback_data='settings_vitrina')
        back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
        markup.add(m1).add(m2).add(m3).add(m4).add(m5, m6).add(m7, m8).add(back)

    await text_editor(text=get.format(wai=''), call=callback_query, markup=markup)


@dp.callback_query_handler(lambda x: x.data.startswith('additional'))
async def change_settings(callback: types.CallbackQuery):
    numbers = callback.data.split('_')
    number = numbers[1]
    category = numbers[2]
    category2 = numbers[3]
    await db.change_sett(user_id=callback.from_user.id, number=number, wai=category)
    await show_additional_buttons(callback_query=callback, category=category2)
