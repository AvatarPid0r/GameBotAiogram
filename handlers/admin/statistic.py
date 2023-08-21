from config.bot_data import db, admin_id, bot
from aiogram import types, Dispatcher
from config.bot_text import text
from datetime import datetime
from markups import cb
import markups as nav
import asyncio

async def send_chat_action(user_id):
    try:
        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.TYPING)
        await asyncio.sleep(0.08)
        return None
    except:
        return user_id

async def statistic_info():
    tasks = []
    data = await db.get_clients_reg_date()
    users = await db.get_all_client()
    date_objects = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f') for date_str in data]
    now = datetime.now()
    count_month, count_day, count_hour, count_all, count_block = 0, 0, 0, len(users), 0
    for date_obj in date_objects:
        if date_obj.year == now.year and date_obj.month == now.month:
            count_month += 1
        if date_obj.year == now.year and date_obj.month == now.month and date_obj.day == now.day:
            count_day += 1
        if date_obj.year == now.year and date_obj.month == now.month and date_obj.day == now.day and date_obj.hour == now.hour:
            count_hour += 1
    for user_id in users:
        tasks.append(asyncio.ensure_future(send_chat_action(user_id)))
    blocked_users = await asyncio.gather(*tasks)
    count_block = len([user_id for user_id in blocked_users if user_id is not None])

    return {"month": count_month, "day": count_day, "hour": count_hour, "block": count_block, "all": count_all}

async def send_statistic(call: types.CallbackQuery):
    await call.answer("⚠️ Вывод статистики может занять немного времени, если в боте много человек!", show_alert=True)
    data = await statistic_info()
    await bot.send_message(call.from_user.id, text.statistic.format(hour=data.get("hour"), day=data.get("day"), month=data.get("month"),
                                                                    block=data.get("block"), all=data.get("all")),
                           reply_markup=nav.back_button("admin_menu"))

async def get_statistic(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "statistic":
        asyncio.create_task(send_statistic(call))


def register_handler_admin_statistic(dp: Dispatcher):
    dp.register_callback_query_handler(get_statistic, cb.filter(action="statistic"), user_id=admin_id)