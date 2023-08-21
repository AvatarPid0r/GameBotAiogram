import json

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.bot_data import db, balance_for_referral, bot, money_name, channel_link
from aiogram import types, Dispatcher
from config.bot_text import text, Text
from config.bot_data import channel
import markups as nav
from utils.message_utils import text_editor
from utils.revenue_send_all import send_all


async def start(message: types.Message, state: FSMContext):
    referrer_id = message.text[7:]
    if not await db.client_exists(message.from_user.id, table="referral"):
        # referrer_id = message.text[7:]
        if referrer_id != "":
            if referrer_id != str(message.from_user.id):
                try:
                    await db.add_client(user_id=message.from_user.id, username=message.from_user.username)
                    await db.add_referral(user_id=message.from_user.id, referrer_id=referrer_id)
                    referrer_balance = await db.get_client_date(referrer_id, ("balance",))
                    new_balance = referrer_balance[0] + balance_for_referral
                    await db.update_data(referrer_id, ("balance", new_balance,))
                    await bot.send_message(referrer_id,
                                           f"🎉 У вас новый реферал(<code>@{message.from_user.username if message.from_user.username is not None else 'Noname'}</code>), "
                                           f"ваш баланс пополнен на <code>{balance_for_referral}</code> {money_name}\n\n На вашем балансе <code>{new_balance}</code> {money_name}",
                                           reply_markup=nav.back_button("main_menu"))
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, "Это ваша же ссылка 😰")
        else:
            await db.add_client(user_id=message.from_user.id, username=message.from_user.username)
    chat_member = await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
    if chat_member.status in ["member", "creator", "administrator"]:
        await bot.send_message(message.from_user.id, text.welcome, reply_markup=nav.welcome_menu(message.from_user.id))
    elif chat_member.status not in ["member", "creator", "administrator"]:
        markup = InlineKeyboardMarkup()
        m1 = InlineKeyboardButton(text='Подписка📌', url=channel_link)
        m2 = InlineKeyboardButton(text='✅ Подписался', callback_data='start')
        markup.add(m2).add(m1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await state.update_data(referrer_id=referrer_id)
        await message.answer(text=Text.dont_subscribe, reply_markup=markup)
        return

async def cheack(callback: types.CallbackQuery):
    await text_editor(call=callback, text=Text.welcome, markup=nav.welcome_menu(callback.from_user.id))


def register_handler_client_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_callback_query_handler(cheack, lambda query: query.data == 'start')
