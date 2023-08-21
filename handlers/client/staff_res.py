from config.bot_data import db, money_name, bot_username, dp, bot
from config.settings_res import *
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav
from config.bot_text import Text


@dp.callback_query_handler(lambda x: x.data.startswith('wait_'))
async def waiter(callback: types.CallbackQuery):
    call = callback.data.split("_")
    wait = call[1]
    if wait == 'oficiant':
        await text_editor(text=Text.oficiant, call=callback, markup=nav.oficiant)
    elif wait == 'sklad':
        await text_editor(text=Text.sklads, call=callback, markup=nav.sklad)
    elif wait == 'kitchen':
        await text_editor(text=Text.citchen, call=callback, markup=nav.citchen)
    elif wait == 'pr':
        await text_editor(text=Text.marketin, call=callback, markup=nav.marketing)
    elif wait == 'administrator':
        await text_editor(text=Text.administrator, call=callback, markup=nav.administration)


@dp.callback_query_handler(lambda x: x.data.startswith('ofic'))
async def oficants(callback: types.CallbackQuery):
    call = callback.data.split('_')
    ofic = call[1]
    wai_dict = {1: (Text.ofic1, limit_hiring_1, (str(buy_oficiant_1) + str(' ' + money_name))),
                2: (Text.ofic2, limit_hiring_2, (str(buy_oficiant_2) + str(' ' + money_name))),
                3: (Text.ofic3, limit_hiring_3, (str(buy_oficiant_3) + str(' ' + money_name)))}
    wai, limit, buy = wai_dict.get(int(ofic))
    m = await db.check_oficiant(user_id=callback.from_user.id, tip=ofic)
    if m:
        await text_editor(text=Text.ofic.format(wai=wai, limit=limit, buy=buy), call=callback,
                          markup=await nav.buyofic(tip=int(ofic)))
    else:
        await bot.answer_callback_query(text=Text.badofic.format(wai=wai, limit=limit, buy=buy), callback_query_id=callback.id, show_alert=True)


@dp.callback_query_handler(lambda x: x.data.startswith('buyofic_'))
async def buy_oficiant(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    await db.buy_ofic(user_id=callback.from_user.id, tip=tip)
    await text_editor(text=Text.buyofic, call=callback, markup=nav.backofic)


@dp.callback_query_handler(lambda x: x.data.startswith('sklad_'))
async def sklad(callback: types.CallbackQuery):
    call = callback.data.split('_')
    sklad = call[1]
    sklad_dict = {1: (Text.sklad1, vessklad_1, (str(buysklad_1) + str(' ' + money_name))),
                  2: (Text.sklad2, vessklad_2, (str(buysklad_2) + str(' ' + money_name))),
                  3: (Text.sklad3, vessklad_3, (str(buysklad_3) + str(' ' + money_name)))}
    wai, limit, buy = sklad_dict.get(int(sklad))
    m = await db.cheack_buy_sklad(user_id=callback.from_user.id, tip=sklad)
    if m:
        await text_editor(text=Text.sklad.format(wai=wai, limit=limit, buy=buy), call=callback,
                          markup=await nav.buysklad(tip=int(sklad)))
    else:
        await text_editor(text=Text.badsklad.format(wai=wai, buy=buy), call=callback, markup=nav.backsklad)


@dp.callback_query_handler(lambda x: x.data.startswith('buysklad_'))
async def buy_sklad(callback: types.CallbackQuery):
    call = callback.data.split('_')
    sklad = call[1]
    await db.buy_sklad(user_id=callback.from_user.id, tip=int(sklad))
    await text_editor(text=Text.buysklad, call=callback, markup=nav.backsklad)


@dp.callback_query_handler(lambda x: x.data.startswith('citchen_'))
async def cheack_cithcen(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    citchen_dict = {1: (Text.citchens1, (str(buycitchen_1) + str(' ' + money_name))),
                    2: (Text.citchens2, (str(buycitchen_2) + str(' ' + money_name))),
                    3: (Text.citchens3, (str(buycitchen_3) + str(' ' + money_name)))}
    wai, buy = citchen_dict.get(int(tip))
    m = await db.cheack_but_citchen(user_id=callback.from_user.id, tip=tip)
    if m:
        await text_editor(text=Text.citchens.format(wai=wai, buy=buy), call=callback,
                          markup=await nav.buycitchen(tip=int(tip)))
    else:
        await text_editor(text=Text.badcitchens.format(wai=wai, buy=buy), call=callback,
                          markup=nav.backcitchen)


@dp.callback_query_handler(lambda x: x.data.startswith('buycitchen_'))
async def buy_citchen(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    await db.buy_citchen(user_id=callback.from_user.id, tip=tip)
    await text_editor(text=Text.buycitchens, call=callback, markup=nav.backcitchen)


@dp.callback_query_handler(lambda x: x.data.startswith('market'))
async def check_marketolog(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    mark_dict = {1: (Text.marketolog1, (str(buymarker_1) + str(' ' + money_name))),
                 2: (Text.marketolog2, (str(buymarker_2) + str(' ' + money_name))),
                 3: (Text.marketolog3, (str(buymarker_3) + str(' ' + money_name)))}
    wai, buy = mark_dict.get(int(tip))
    m = await db.cheack_but_marketologa(user_id=callback.from_user.id, tip=tip)
    if m:
        await text_editor(text=Text.marketolog.format(wai=wai, buy=buy), call=callback,
                          markup=await nav.buymarketol(tip=int(tip)))
    else:
        await text_editor(text=Text.badmarketolog.format(wai=wai, buy=buy), call=callback,
                          markup=nav.backmarketol)


@dp.callback_query_handler(lambda x: x.data.startswith('buymarketolog_'))
async def but_marketolog(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    await db.buy_marketologs(user_id=callback.from_user.id, tip=tip)
    await text_editor(text=Text.buymarketolog, call=callback, markup=nav.backmarketol)


@dp.callback_query_handler(lambda x: x.data.startswith('admin_'))
async def cheack_admin(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    admin_dict = {1: (Text.administrators1, (str(buyadmin_1) + str(' ' + money_name))),
                  2: (Text.administrators2, (str(buyadmin_2) + str(' ' + money_name))),
                  3: (Text.administrators3, (str(buyadmin_3) + str(' ' + money_name)))}
    wai, buy = admin_dict.get(int(tip))
    m = await db.cheack_buy_administ(user_id=callback.from_user.id, tip=tip)
    if m:
        await text_editor(text=Text.administrators.format(wai=wai, buy=buy), call=callback,
                          markup=await nav.buyadmins(tip=int(tip)))
    else:
        await text_editor(text=Text.badadministrators.format(wai=wai, buy=buy), call=callback,
                          markup=nav.backadmins)


@dp.callback_query_handler(lambda x: x.data.startswith('buyadminist_'))
async def buy_admin(callback: types.CallbackQuery):
    call = callback.data.split('_')
    tip = call[1]
    await db.buy_admin(user_id=callback.from_user.id, tip=tip)
    await text_editor(text=Text.buyadministrators, call=callback, markup=nav.backadmins)



@dp.callback_query_handler(lambda x: x.data.startswith('top_') or x.data == 'show_top')
async def get_top(callback: types.CallbackQuery):
    call = callback.data.split('_')
    top = call[1]
    if callback.data == 'show_top':
        await text_editor(text=text.show_top, call=callback, markup=nav.show_top)
        return
    m = await db.get_top(privod=top)
    if not m:
        await bot.answer_callback_query(callback_query_id=callback.id, text=text.bad_top, show_alert=True)
    if top == 'day':
        texts = text.top_day
    elif top == 'week':
        texts = text.top_week
    elif top == 'month':
        texts = text.top_month
    for rank, (user_id, score) in enumerate(m, start=1):
        texts += text.text_for_send_top.format(count=rank, username=user_id, money=score)


    await text_editor(text=texts, call=callback, markup=nav.show_top)







