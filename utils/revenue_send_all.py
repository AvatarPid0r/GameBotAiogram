import asyncio

from aiogram.dispatcher import FSMContext
import json
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
from utils.reporting import cheac_review, cheack_events
import datetime


async def send_all():
    try:
        result = await db.cheack_all()
        for user_id in result:
            user_id = user_id[0]
            result = await db.res_revenue(user_id=user_id)
            await bot.send_message(text=text.count_prodash.format(all_balance=result.get('all_balance'),
                                                                  all_sell_product=result.get('all_sell_product'),
                                                                  zakus=result.get('zakus'),
                                                                  napitki=result.get('napitki'),
                                                                  skacs=result.get('skacs'),
                                                                  deserts=result.get('deserts'),
                                                                  zakus_money=result.get('zakus_money'),
                                                                  napitki_money=result.get('napitki_money'),
                                                                  snacks_money=result.get('snacks_money'),
                                                                  deserts_money=result.get('deserts_money'),
                                                                  money=result.get('referall_money'),
                                                                  plata_job_oficiant=result.get('plata_job_oficiant'),
                                                                  plata_job_market=result.get('plata_job_market'),
                                                                  plata_job_chefs=result.get('plata_job_chefs'),
                                                                  plata_job_admin=result.get('plata_job_admin'),
                                                                  all_client=result.get('all_client'),
                                                                  money_conflict=result.get('money_conflict'),
                                                                  all_client_yes=result.get('all_client_yes'),
                                                                  count_conflict=result.get('count_conflict')),
                                   chat_id=user_id)

            await cheac_review(user_id=user_id)
            results = await db.read_review(user_id=user_id)
            result_dict = json.loads(results)
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

            await bot.send_message(chat_id=user_id, text=text.review_send + text_send)

            event_dict = await cheack_events(shefs_no_product=result.get('shefs_no_product'),
                                             del_oficiant=result.get('del_oficiant'),
                                             no_market_client=result.get('no_market_client'),
                                             market_client=result.get('market_client'),
                                             up_product_citchen=result.get('up_product_citchen'),
                                             del_product_sklad=result.get('del_product_sklad'),
                                             admin_fart=result.get('admin_fart'))
            event_spisoc = []
            for i in event_dict.values():
                event_spisoc.append(i)

            count = 0
            text_sends = ""
            for i in event_spisoc:
                count += 1
                text_sends += f'{count}. <i>{i}</i>\n'

            await bot.send_message(chat_id=user_id, text=text.event_send + text_sends, reply_markup=nav.back_button(value='main_menu'))
    except:
        pass

async def check_time_and_send():
    while True:
        now = datetime.datetime.now()
        hour = now.hour

        if hour == send_all_task:
            await send_all()
            await asyncio.sleep(4000)

        await asyncio.sleep(60)
