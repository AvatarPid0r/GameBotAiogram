import asyncio
import os
import random

from aiogram.dispatcher import FSMContext

from states.states import Admin
from utils.message_utils import text_editor
from aiogram import types, Dispatcher
from config.bot_data import admin_id, dp, db, bot
from config.bot_text import text
from markups import cb
import markups as nav
from utils.revenue_send_all import send_all


@dp.callback_query_handler(lambda x: x.data == 'create_event', state='*')
async def create_event(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
    client, balance, fart, fart_text, no_fart_text, status = await db.cheack_event()
    if status == 0:
        await text_editor(text=text.creates_event, call=callback, markup=nav.events)
    else:
        await text_editor(text=text.cheack_event.format(up_client=client, balance=balance,
                                                        fart=fart, fart_text=fart_text,
                                                        no_fart_text=no_fart_text), call=callback, markup=nav.events)


@dp.callback_query_handler(lambda x: x.data in ('up_client', 'event_balance', 'fart_event', 'event_yes', 'event_no'))
async def change_event(callback: types.CallbackQuery, state: FSMContext):
    await text_editor(text=text.change_event, call=callback, markup=nav.backevent)
    await state.update_data(event=callback.data)
    await Admin.CreateEvent.text.set()


@dp.message_handler(state=Admin.CreateEvent.text)
async def change_events(message: types.Message, state: FSMContext):
    data = await state.get_data()
    m = await db.create_event(event=data.get('event'), text=message.text)
    client, balance, fart, fart_text, no_fart_text, status = await db.cheack_event()
    if m == True:
        await text_editor(text=text.cheack_event.format(up_client=client, balance=balance,
                                                        fart=fart, fart_text=fart_text,
                                                        no_fart_text=no_fart_text), message=message, markup=nav.events)
        await state.finish()
    else:
        await text_editor(text=text.cheack_event.format(up_client=client, balance=balance,
                                                        fart=fart, fart_text=fart_text,
                                                        no_fart_text=no_fart_text) + str(m), message=message, markup=nav.events)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'event_send')
async def event_send(callback: types.CallbackQuery):
    client, balance, fart, fart_text, no_fart_text, status = await db.cheack_event()
    if client == 0 and balance == 0:
        await bot.answer_callback_query(callback_query_id=callback.id, text='❌ Для начала укажите "Баланс" или же "Клиентов в сутки"', show_alert=True)
        return
    elif fart == 0:
        await bot.answer_callback_query(callback_query_id=callback.id,
                                        text='❌ Для отправки события вам нужно указать процент фарта', show_alert=True)
        return
    await text_editor(text=text.confirm_event.format(up_client=client, balance=balance,
                                                        fart=fart, fart_text=fart_text,
                                                        no_fart_text=no_fart_text), call=callback, markup=nav.confirm_event)


@dp.callback_query_handler(lambda x: x.data == 'send_event_all')
async def event_send_all(callback: types.CallbackQuery):
    client, balance, fart, fart_text, no_fart_text, status = await db.cheack_event()
    users = await db.get_all_client()
    successful_users = 0  # Количество пользователей, кому удалось отправить сообщение
    unsuccessful_users = 0  # Количество пользователей, кому не удалось отправить сообщение

    for user_id in users:
        result = await send_all_event(user_id=int(user_id), fart=fart_text, no_fart=no_fart_text, shanc=int(fart))
        if result:
            successful_users += 1
        else:
            unsuccessful_users += 1
    await text_editor(text=text.cheack_event.format(up_client=client, balance=balance,
                                                    fart=fart, fart_text=fart_text,
                                                    no_fart_text=no_fart_text) + '\n\nДождитесь пока все события сыграют, вам придет уведомление', call=callback, markup=nav.backevent)

    message = f"Удалось отправить {successful_users} сообщений. Кому повезло: {successful_users}. Кому не повезло: {unsuccessful_users}."
    await bot.send_message(chat_id=callback.from_user.id, text=message)






async def send_all_event(user_id: int, fart: str, no_fart: str, shanc: int):
    client, balance, farts, fart_text, no_fart_text, status = await db.cheack_event()
    try:
        m1 = random.randint(0, 100)
        if shanc >= m1:
            await bot.send_message(chat_id=int(user_id), text=fart, reply_markup=nav.back_button(value='main_menu'))
            await db.event_save(user_id=int(user_id), balance=balance, client=client)
            return True
        else:
            await bot.send_message(chat_id=int(user_id), text=no_fart, reply_markup=nav.back_button(value='main_menu'))
            await db.event_save(user_id=int(user_id), balance=(int(balance)-int(balance)-int(balance)), client=(int(client)-int(client)-int(client)))
            return False
    except:
        return user_id

