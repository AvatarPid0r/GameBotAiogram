from config.bot_data import money_name, admin_id, db
from utils.message_utils import text_editor
from aiogram.dispatcher import FSMContext
from handlers.admin import promo, tasks
from aiogram import types, Dispatcher
from config.bot_text import text

import markups as nav


async def back_handler(call: types.CallbackQuery, state: FSMContext):
    action = call.data[5:]
    if action == "main_menu":
        if await state.get_state() is not None:
            await state.finish()
        await text_editor(text=text.main_menu.format(money_name=money_name),
                          call=call,
                          markup=nav.main_menu(call.from_user.id))
    elif action == "earn_menu":
        await text_editor(text=text.earn, call=call, markup=nav.earn_keyboard)
    elif action == "admin_menu" and call.from_user.id in admin_id:
        if await state.get_state() is not None:
            await state.finish()
        await text_editor(text=text.admin_menu.format(name=call.from_user.first_name), call=call, markup=nav.admin_menu)
    elif action == "add_channel_menu" and call.from_user.id in admin_id:
        await tasks.update_data(state)
        await text_editor(text=text.add_task_menu, call=call, markup=nav.add_task_menu)
    elif action == "add_promo_menu" and call.from_user.id in admin_id:
        await promo.update_data(state)
        await text_editor(text=text.add_promo_menu, call=call, markup=nav.promo_menu)
    elif action == 'product':
        if await state.get_state() is not None:
            await state.finish()
        zakus, napitki, snack, desert, sklad, sklad_all, cheack_client = await db.get_products(call.from_user.id)

        sklad_all = sklad - sklad_all

        await text_editor(text=text.product.format(zakus=zakus,
                                                   napitki=napitki,
                                                   snacks=snack,
                                                   desers=desert,
                                                   sklad=sklad,
                                                   sklad_all=sklad_all), call=call, markup=nav.product_keyboard)


def register_handler_client_back(dp: Dispatcher):
    dp.register_callback_query_handler(back_handler, text_contains="back|", state="*")
