from config.bot_data import db, money_name, bot_username, dp, bot
from config.settings_res import *
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav
from config.bot_text import Text


@dp.callback_query_handler(lambda x: x.data.startswith('improvement_'))
async def buy_improvement(callback: types.CallbackQuery):
    calls = callback.data.split('_')
    call = calls[1]
    if call.isdigit():
        m = await db.check_improvement(user_id=callback.from_user.id, product=call)
        if int(call) == 4 and m == False:
            await bot.answer_callback_query(text=text.bad_buy_improvement4, callback_query_id=callback.id, show_alert=True)
            return
        if m == False:
            await bot.answer_callback_query(text=text.bad_buy_improvement, callback_query_id=callback.id,
                                            show_alert=True)
            return
        product = int(call)
        text_desc = getattr(text, f"improvement{product}_decs", text.improvement)
        markup = await nav.confirm_improvement(product=product)
    else:
        text_desc = text.improvement
        markup = await nav.improvement_markup(user_id=callback.from_user.id)

    await text_editor(text=text_desc, call=callback, markup=markup)


@dp.callback_query_handler(lambda x: x.data.startswith('improvementconfirm_'))
async def buy_improvement(callback: types.CallbackQuery):
    calls = callback.data.split('_')
    call = calls[1]
    m = await db.buy_improvement(user_id=callback.from_user.id, product=int(call))
    await bot.answer_callback_query(text=text.good_buy_improvement, callback_query_id=callback.id, show_alert=True)
    await text_editor(text=text.improvement, call=callback,
                      markup=await nav.improvement_markup(user_id=callback.from_user.id))
