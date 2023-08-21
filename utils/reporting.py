import os

from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from itertools import islice
from config.bot_text import Text as text
from config.bot_data import db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.bot_data import procent_to_referal
import random

review_all = os.path.join(os.getcwd(), "text_for_review")
events_all = os.path.join(os.getcwd(), "events_text")


async def cheac_review(user_id: int):
    review = {}

    async def get_random_line(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_line = random.choice(lines).strip()
            index = len(review) + 1
            review[index] = random_line

    count_oficant_1, count_oficant_2, count_oficant_3, \
    count_all_admin, count_all_market, count_product_1, \
    count_product_2, count_product_3, count_product_4, \
    settings_1, settings_2, settings_3, settings_4, result_product = await db.review(user_id=user_id)

    if count_oficant_1 and count_oficant_2 and count_oficant_3:
        review_paths = [
            os.path.join(review_all, 'Для официантов професионалов.txt'),
            os.path.join(review_all, 'Для офицантов любителей.txt'),
            os.path.join(review_all, 'Для офицантов новичков.txt')
        ]
        await get_random_line(random.choice(review_paths))
    elif count_oficant_1 and count_oficant_2:
        review_paths = [
            os.path.join(review_all, 'Для офицантов любителей.txt'),
            os.path.join(review_all, 'Для офицантов новичков.txt')
        ]
        await get_random_line(random.choice(review_paths))
    elif count_oficant_3:
        await get_random_line(os.path.join(review_all, 'Для официантов професионалов.txt'))
    elif count_oficant_2:
        await get_random_line(os.path.join(review_all, 'Для офицантов любителей.txt'))
    elif count_oficant_1:
        await get_random_line(os.path.join(review_all, 'Для офицантов новичков.txt'))

    if count_all_admin:
        await get_random_line(os.path.join(review_all, 'Есть администраторы.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету администраторов.txt'))

    if count_all_market:
        await get_random_line(os.path.join(review_all, 'Есть маркетологи.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету маркетологов.txt'))

    if count_product_1:
        await get_random_line(os.path.join(review_all, 'Есть закуски.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету закусков.txt'))

    if count_product_2:
        await get_random_line(os.path.join(review_all, 'Есть напитки.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету напитков.txt'))

    if count_product_3:
        await get_random_line(os.path.join(review_all, 'Есть снеки.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету снеков.txt'))

    if count_product_4:
        await get_random_line(os.path.join(review_all, 'Есть десерты.txt'))
    else:
        await get_random_line(os.path.join(review_all, 'Нету десертов.txt'))

    if settings_1 == 2:
        await get_random_line(os.path.join(review_all, 'Хитрости переливать.txt'))
    elif settings_1 == 3:
        await get_random_line(os.path.join(review_all, 'Хитрости недоливать.txt'))

    if settings_2 == 2:
        await get_random_line(os.path.join(review_all, 'Ценообразие цена выше.txt'))
    elif settings_2 == 3:
        await get_random_line(os.path.join(review_all, 'Ценообразие цена ниже.txt'))

    if settings_3 == 2:
        await get_random_line(os.path.join(review_all, 'Настройка3 кнопка3.txt'))
    elif settings_3 == 3:
        await get_random_line(os.path.join(review_all, 'Настройка3 кнопка2.txt'))
    elif settings_3 == 4:
        await get_random_line(os.path.join(review_all, 'Настройка3 кнопка1.txt'))

    if settings_4 == 2:
        await get_random_line(os.path.join(review_all, 'Настройка4 кнопка3.txt'))
    elif settings_4 == 3:
        await get_random_line(os.path.join(review_all, 'Настройка4 кнопка2.txt'))
    elif settings_4 == 4:
        await get_random_line(os.path.join(review_all, 'Настройка4 кнопка1.txt'))

    if result_product == True:
        await get_random_line(os.path.join(review_all, 'Все продукты.txt'))

    await db.write_review(user_id=int(user_id), review=review)


async def cheack_events(shefs_no_product, del_oficiant, no_market_client, market_client, up_product_citchen,
                        del_product_sklad, admin_fart):
    event = {}
    async def get_random_line(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_line = random.choice(lines).strip()
            index = len(event) + 1
            event[index] = random_line

    if shefs_no_product == 1:
        await get_random_line(os.path.join(events_all, 'Кухня не удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_citchen

    if del_oficiant == 1:
        await get_random_line(os.path.join(events_all, 'Официанты не удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_oficiant

    if no_market_client == 1:
        await get_random_line(os.path.join(events_all, 'Маркетологи не удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_market
    if market_client == 1:
        await get_random_line(os.path.join(events_all, 'Маркетологи удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_market

    if up_product_citchen == 1:
        await get_random_line(os.path.join(events_all, 'Кухня удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_citchen

    if del_product_sklad == 1:
        await get_random_line(os.path.join(events_all, 'Склад не удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_sklad

    if admin_fart == 1:
        await get_random_line(os.path.join(events_all, 'Административный отдел не удача.txt'))
    elif admin_fart == 2:
        await get_random_line(os.path.join(events_all, 'Административный отдел удача.txt'))
    else:
        index = len(event) + 1
        event[index] = text.no_event_admin

    return event







