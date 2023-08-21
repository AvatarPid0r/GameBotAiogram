from utils.message_utils import text_editor
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from config.bot_text import text
from states.states import Client
from config.bot_data import db
from markups import cb
import markups as nav


async def promo_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "enter_promocode":
        await text_editor(text=text.promo_change_promo, call=call, markup=nav.back_button("main_menu"))
        await Client.Promo.get_promo.set()

async def enter_promo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["promo"] = message.text.lower()
    if not await db.promo_exists(data["promo"]):
        await text_editor(text=text.promo_not_exist, message=message, markup=nav.back_button("main_menu"))
        return
    if await db.is_promo_used(message.from_user.id, data["promo"]):
        await text_editor(text=text.promo_used, message=message, markup=nav.back_button("main_menu"))
        return
    client_balance = (await db.get_client_date(message.from_user.id, ("balance",)))[0]
    promo_reward = await db.get_promo_reward(data["promo"])
    await db.update_data(message.from_user.id, ("balance", client_balance+promo_reward))
    await db.add_entered_promo(message.from_user.id, data["promo"])
    await text_editor(text=text.successful_promo.format(reward=promo_reward), message=message, markup=nav.back_button("main_menu"))
    await state.finish()


def register_handler_client_promo(dp: Dispatcher):
    dp.register_callback_query_handler(promo_menu, cb.filter(action=["enter_promocode"]))
    dp.register_message_handler(enter_promo, state=Client.Promo.get_promo)