import hashlib
import logging

from aiogram.dispatcher import FSMContext

from config.bot_data import db, money_name, min_withdraw, min_referrer_withdraw, redirect_link, db_json, bot, dp, \
    items_per_page, channel_for_log
from config.settings_res import obmen, min_obmen
from states.states import Client
from utils.message_utils import text_editor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.paginations import PaginationPartner, PaginationCert

user_pages = {}
user_pages_cert = {}
user_pages_cert_part = {}


@dp.callback_query_handler(lambda c: c.data in ["withdraw", "prev_page", "next_page", 'none'])
async def withdraw(call: types.CallbackQuery):
    global user_pages_cert, user_pages_cert_part
    names = await db_json.cheack_all_partner()
    pagination = PaginationPartner(items_per_page, names)

    user_id = call.from_user.id

    if user_id not in user_pages:
        user_pages[user_id] = 1

    current_page = user_pages[user_id]

    if call.data == "prev_page":
        current_page -= 1
        if current_page < 1:
            current_page = 1

    if call.data == "next_page":
        current_page += 1
        page_count = pagination.get_page_count()

    user_pages[user_id] = current_page

    if call.data == 'none':
        await bot.answer_callback_query(text='❌ Достигнут предел страниц', callback_query_id=call.id)
        return

    if call.data == "withdraw":
        user_pages_cert = {}
        user_pages_cert_part = {}


    markup = pagination.get_pagination_markup(current_page)
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))

    await text_editor(text=text.withdraw.format(link=redirect_link), call=call, markup=markup)


@dp.callback_query_handler(lambda x: x.data.startswith('partner_') or x.data in ['prepagecert', 'nextpagecert'])
async def cert_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    call = callback.data.split('_')
    try:
        partner = call[1]
        if callback.from_user.id not in user_pages_cert_part:
            user_pages_cert_part[user_id] = partner
    except:
        pass
    partner = user_pages_cert_part[user_id]
    names, price = await db_json.cheack_all_cert(name=partner)
    if names == []:
        await bot.answer_callback_query(text='❌ Список сертификатов пуст', callback_query_id=callback.id)
        return
    pagination = PaginationCert(items_per_page=items_per_page, names=names, partner=partner, price=price)

    user_id = callback.from_user.id

    if user_id not in user_pages_cert:
        user_pages_cert[user_id] = 1
        user_pages_cert_part[user_id] = partner

    current_page = user_pages_cert[user_id]

    if callback.data == "prepagecert":
        current_page -= 1
        if current_page < 1:
            current_page = 1

    if callback.data == "nextpagecert":
        current_page += 1
        page_count = pagination.get_page_count()

    user_pages_cert[user_id] = current_page

    markup = pagination.get_pagination_markup(current_page)
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data=f"withdraw"))

    await text_editor(text=text.spisok.format(partner=partner), call=callback, markup=markup)


@dp.callback_query_handler(lambda x: x.data.startswith('buycert_'))
async def buy_cert(callback: types.CallbackQuery, state: FSMContext):
    call = callback.data.split('_')
    partner = call[1]
    name = call[2]
    price = await db_json.cheack_price(name=name, partner=partner)
    cheack = await db.cheack_balance(user_id=callback.from_user.id, price=price)
    if cheack == False:
        await bot.answer_callback_query(text=text.bad_but_cert.format(buy=price), callback_query_id=callback.id,
                                        show_alert=True)
        return
    await state.update_data(names=name)
    await state.update_data(partners=partner)
    await state.update_data(price=price)

    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton(text="🔙 Назад", callback_data=f"partner_{partner}")
    m2 = InlineKeyboardMarkup(text='Да', callback_data=f'yes_{partner}_{name}')
    markup.add(m2).add(m1)
    await text_editor(text=text.buy_certss.format(name=name,
                                                partner=partner,
                                                money=price), call=callback, markup=markup)


@dp.callback_query_handler(lambda x: x.data.startswith('yes_'))
async def buy(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('names')
    partner = data.get('partners')
    price = data.get('price')
    await db.buy_promocode(user_id=callback.from_user.id, price=int(price))
    url, promocode = await db_json.del_certif_but(partner=partner, name=name)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    message = await bot.send_message(text=text.send_cert.format(partner=partner,
                                                      name=name,
                                                      promocode=promocode,
                                                      url=url), chat_id=callback.from_user.id)
    await bot.pin_chat_message(chat_id=callback.from_user.id, message_id=message.message_id)
    await bot.send_message(callback.from_user.id, text.welcome, reply_markup=nav.welcome_menu(callback.from_user.id))

@dp.callback_query_handler(lambda x: x.data == 'show_calc')
async def show(callback: types.CallbackQuery):
    await text_editor(text=text.show_calc, call=callback, markup=nav.show_vivod)

@dp.inline_handler()
async def inline_calculator(query: types.InlineQuery):
    try:
        text = query.query or 'Echo'
        text = (text.split('='))[1]
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        if not text:
            return

        rubles = int(text)
        usd = rubles / obmen
        if rubles < 1000:
            result = f'❌ Минимальная сумма обмена 1000 {money_name} = 1 RUB'
            desc = ''
        else:
            result = f'{int(rubles)} {money_name} = {int(usd)} RUB'
            desc = '✅ Нажми сюда чтобы выбрать данную сумму'

        article = types.InlineQueryResultArticle(
            id=result_id,
            title=result,
            input_message_content=types.InputTextMessageContent(f'VAL_RUB={int(usd)}'),
            description=desc
        )
        await bot.answer_inline_query(query.id, results=[article], cache_time=1)
    except:
        pass

@dp.message_handler(regexp=r'^VAL_RUB=')
async def card(message: types.Message, state: FSMContext) -> None:
    rub = message.text
    rub = (rub.split('='))[1]
    m = await db.cheack_balance(user_id=message.from_user.id, price=(int(rub) * obmen))
    if int(rub) < int(min_obmen):
        await text_editor(text=text.min_card, message=message, markup=nav.back_button(value='main_menu'))
        return

    if m == False:
        await text_editor(text=text.bad_card, message=message, markup=nav.back_button(value='main_menu'))
        return
    await text_editor(text=text.card, message=message, markup=nav.back_button(value='main_menu'))
    await state.update_data(rub=rub)
    await Client.Card.recv.set()


@dp.message_handler(state=Client.Card.recv)
async def cheack_recv(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    rub = data.get('rub')
    val = int(rub) * obmen
    card = message.text

    username = message.from_user.username

    if username is None:
        username = "None"

    keyboard = InlineKeyboardMarkup(row_width=1)
    m1 = InlineKeyboardButton('✅ Подтвердить', callback_data=f'vivod_{rub}_{val}_{message.from_user.id}_{username}_{card}')
    m2 = InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu")
    keyboard.add(m1, m2)
    await text_editor(text=text.cheack_recv.format(card=card,
                                                   rub=rub,
                                                   money=val), message=message, markup=keyboard)
    await state.finish()

@dp.callback_query_handler(lambda x: x.data.startswith('vivod'))
async def vivod(callback: types.CallbackQuery):
    call = callback.data.split('_')
    rub = call[1]
    val = call[2]
    user_id = call[3]
    username = call[4]
    card = call[5]
    await db.minus_balance(user_id=user_id, price=val)
    await text_editor(text=text.good_card.format(rub=rub, card=card), call=callback, markup=nav.back_button(value='main_menu'))
    await bot.send_message(chat_id=channel_for_log, text=text.zayavka_vivod.format(user_id=user_id,
                                                                                   username=username,
                                                                                   rub=rub,
                                                                                   card=card))




























