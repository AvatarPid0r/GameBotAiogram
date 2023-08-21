from aiogram.dispatcher import FSMContext

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


@dp.callback_query_handler(lambda x: x.data.startswith('buy_'))
async def buyproduct(callback: types.CallbackQuery, state: FSMContext):
    call = callback.data.split('_')
    product = call[2]
    product_dict = {1: Text.zakus, 2: Text.napitk, 3: Text.snacks, 4: Text.deserts}
    texts = product_dict.get(int(product))

    await text_editor(text=texts, call=callback, markup=nav.backproduct)
    await state.update_data(product=int(product))
    await Product.text.set()


@dp.message_handler(state=Product.text)
async def confirm_purchase(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = data.get('product')
    count = message.text
    if not message.text.isdigit():
        await text_editor(text=Text.noisidigitproduct, message=message, markup=nav.backproduct)
        return
    m = await db.check_purchase(user_id=message.from_user.id, product=product, count=count)

    if m == '':
        price: int = int(count) * int(globals()[f'buyproduct_{product}'])
        text = {1: Text.product_to_good_1, 2: Text.product_to_good_2, 3: Text.product_to_good_3, 4: Text.product_to_good_4}
        texts = text.get(int(product))
        await text_editor(text=Text.product_confirm.format(count=count, product=texts, money=price), markup=await nav.confirm_product(product=product, count=count),
                          message=message)
        await state.finish()
    else:
        await text_editor(text=m, message=message, markup=nav.backproduct)


@dp.callback_query_handler(lambda x: x.data.startswith('confirm_'))
async def handle_confirmation(callback: types.CallbackQuery, state: FSMContext):
    call = callback.data.split('_')
    product = call[1]
    count = call[2]

    m = await db.buy_product(user_id=callback.from_user.id, product=product, count=count)

    if m == True:
        await text_editor(text=Text.buygoodproduct, call=callback, markup=nav.backproduct)
    else:
        await text_editor(text=m, call=callback, markup=nav.backproduct)

    await state.finish()
