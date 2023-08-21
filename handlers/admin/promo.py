from utils.message_utils import text_editor
from aiogram.dispatcher import FSMContext
from config.bot_data import admin_id, db
from aiogram import types, Dispatcher
from config.bot_text import text
from states.states import Admin
from markups import cb
import markups as nav


async def update_data(state: FSMContext):
    data = await state.get_data()
    await state.finish()
    await Admin.AddPromo.data.set()
    await state.update_data(promo=data.get("promo"), reward=data.get("reward"))

async def promo_handler(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "create_promo":
        await text_editor(text=text.add_promo_menu, call=call, markup=nav.promo_menu)
    elif action == "delete_promo":
        await text_editor(text=text.promo_change_promo, call=call, markup=nav.back_button("admin_menu"))
        await Admin.DeletePromo.get_promo.set()

async def add_promo_data(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "enter_reward":
        await text_editor(text=text.promo_change_reward, call=call, markup=nav.back_button("add_promo_menu"))
        await Admin.AddPromo.get_reward.set()
    if action == "enter_promo":
        await text_editor(text=text.promo_change_promo, call=call, markup=nav.back_button("add_promo_menu"))
        await Admin.AddPromo.get_promo.set()
    if action == "publish_promo":
        data = await state.get_data()
        if not (data.get("promo") and data.get("reward")):
            await call.answer(text.promo_dont_filled, show_alert=True)
            return
        try:
            await db.add_promo(data.get("promo"), data.get("reward"))
            await call.answer(text.promo_added, show_alert=True)
        except:
            await call.answer("Произошла ошибка, промокод не сохранен", show_alert=True)
        await text_editor(text=text.admin_menu, call=call, markup=nav.admin_menu)
        await state.finish()

async def get_del_promo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo"] = message.text.lower()
    if not await db.promo_exists(data["promo"]):
        await text_editor(text=text.promo_not_exist, message=message, markup=nav.back_button("admin_menu"))
        return
    await db.delete_promo(data["promo"])
    await text_editor(text=text.admin_menu, message=message, markup=nav.admin_menu)

async def get_reward(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["reward"] = message.text
    if not data["reward"].isdigit():
        await text_editor(text=text.incorrect_reward_type, message=message, markup=nav.back_button("add_promo_menu"))
        return
    await text_editor(text=text.add_promo_menu, message=message, markup=nav.promo_menu)
    await update_data(state)

async def get_promocode(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo"] = message.text
    await text_editor(text=text.add_promo_menu, message=message, markup=nav.promo_menu)
    await update_data(state)


def register_handler_admin_promo(dp: Dispatcher):
    dp.register_callback_query_handler(promo_handler, cb.filter(action=["create_promo", "delete_promo"]), user_id=admin_id)
    dp.register_callback_query_handler(add_promo_data, cb.filter(action=["enter_reward", "enter_promo", "publish_promo"]), state="*", user_id=admin_id)
    dp.register_message_handler(get_reward, state=Admin.AddPromo.get_reward, user_id=admin_id)
    dp.register_message_handler(get_promocode, state=Admin.AddPromo.get_promo, user_id=admin_id)
    dp.register_message_handler(get_del_promo, state=Admin.DeletePromo.get_promo, user_id=admin_id)
