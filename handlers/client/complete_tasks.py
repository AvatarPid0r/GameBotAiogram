from utils.message_utils import text_editor, admin_send_message
from config.bot_data import db, money_name, bot, dp
from utils.paginations import Paginator
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav


async def task_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "tasks":
        data = await db.get_task_data(completed_tasks=await db.get_completed_tasks(call.from_user.id))
        if len(data) == 0:
            await text_editor(text=text.no_task, call=call, markup=nav.back_button("earn_menu"))
            return
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            *[types.InlineKeyboardButton(f"👉 Задание {index}", callback_data=f"task|{index}") for index in data.keys()])
        paginator = Paginator(data=kb, size=10, dp=dp, back_callback="earn_menu")
        await text_editor(text=text.choose_task, call=call, markup=paginator())


async def tasks_list(call: types.CallbackQuery):
    task_id = call.data[5:]
    if task_id in await db.get_completed_tasks(call.from_user.id):
        await text_editor(text=text.uncompleted_task, call=call, markup=nav.back_button("earn_menu"))
        return
    task_data = await db.get_task_data(task_id=task_id)
    try:
        await text_editor(text=text.task_text.format(task_id=task_id, description=task_data.get("description"),
                                                     reward=task_data.get("reward"), money_name=money_name),
                          call=call, markup=nav.complete_task_menu(task_id))
    except:
        await text_editor(text=text.uncompleted_task, call=call, markup=nav.back_button("earn_menu"))
        await admin_send_message(f"Невозможно спарсить задание с ID: <code>{task_id}</code>")


async def check_task(call: types.CallbackQuery):
    task_id = call.data[6:]
    task_data = await db.get_task_data(task_id=task_id)
    if task_id in await db.get_completed_tasks(call.from_user.id):
        await call.answer(text.uncompleted_task, show_alert=True)
        return
    if not task_data.get("channel_id"):
        await call.answer(text.task_not_complete, show_alert=True)
        return
    try:
        user_channel_status = await bot.get_chat_member(chat_id=task_data.get("channel_id"), user_id=call.from_user.id)
    except:
        await admin_send_message(text.error_with_task.format(channel_id=task_data.get("channel_id")))
        return
    if user_channel_status["status"] == "left":
        await call.answer(text.dont_subscribe, show_alert=True)
        return
    client_data = (await db.get_client_date(call.from_user.id, ("balance",)))[0]
    await db.update_data(call.from_user.id, ("balance", client_data + task_data.get("reward")))
    await db.add_completed_task(call.from_user.id, task_id)
    await text_editor(text=text.successful_task.format(task_id=task_id), call=call, markup=nav.back_button("earn_menu"))


def register_handler_client_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(task_menu, cb.filter(action=["tasks"]))
    dp.register_callback_query_handler(tasks_list, text_contains="task|")
    dp.register_callback_query_handler(check_task, text_contains="check|")
