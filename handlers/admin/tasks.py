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
    await Admin.AddTask.data.set()
    await state.update_data(reward=data.get("reward"), description=data.get("description"), channel_id=data.get("channel_id"))

async def task_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "add_task":
        await text_editor(text=text.add_task_menu, call=call, markup=nav.add_task_menu)
    if action == "delete_task":
        await text_editor(text=text.task_id, call=call, markup=nav.back_button("admin_menu"))
        await Admin.DeleteTask.task_id.set()

async def add_task_data(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "change_description":
        await text_editor(text=text.task_change_description, call=call, markup=nav.back_button("add_channel_menu"))
        await Admin.AddTask.description.set()
    if action == "change_reward":
        await text_editor(text=text.task_change_reward, call=call, markup=nav.back_button("add_channel_menu"))
        await Admin.AddTask.reward.set()
    if action == "change_channel_id":
        await text_editor(text=text.task_change_channel_id, call=call, markup=nav.back_button("add_channel_menu"))
        await Admin.AddTask.task_id.set()
    if action == "publish_task":
        data = await state.get_data()
        if not(data.get("description") and data.get("reward")):
            await call.answer(text.task_not_filled, show_alert=True)
            return
        try:
            await db.add_task(data.get("description"), data.get("reward"), data.get("channel_id"))
            await call.answer(text.task_added, show_alert=True)
        except:
            await call.answer("Произошла ошибка, задание не сохранено", show_alert=True)
        await text_editor(text=text.admin_menu.format(name=call.from_user.first_name), call=call,
                          markup=nav.admin_menu)
        await state.finish()


async def get_task_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["task_id"] = message.text
    if not data["task_id"].isdigit():
        await text_editor(text=text.incorrect_task_type, message=message, markup=nav.back_button("admin_menu"))
        return
    if not await db.task_exists(data["task_id"]):
        await text_editor(text=text.task_not_exist, message=message, markup=nav.back_button("admin_menu"))
        return
    try:
        await db.delete_task(data["task_id"])
    except: pass
    await text_editor(text=text.admin_menu.format(name=message.from_user.first_name), message=message, markup=nav.admin_menu)
    await state.finish()

async def change_reward(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["reward"] = message.text
    if not data["reward"].isdigit():
        await text_editor(text=text.incorrect_reward_type, message=message, markup=nav.back_button("add_channel_menu"))
        return
    await text_editor(text=text.add_task_menu, message=message, markup=nav.add_task_menu)
    await update_data(state)

async def change_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await text_editor(text=text.add_task_menu, message=message, markup=nav.add_task_menu)
    await update_data(state)

async def change_channel_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["channel_id"] = message.text
    if not(data["channel_id"][0] == "-" and data["channel_id"][1:].isdigit()):
        await text_editor(text=text.not_valid_id, message=message, markup=nav.back_button("add_channel_menu"))
        return
    await text_editor(text=text.add_task_menu, message=message, markup=nav.add_task_menu)
    await update_data(state)

def register_handler_admin_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(task_menu, cb.filter(action=["add_task", "delete_task"]), state="*", user_id=admin_id)
    dp.register_callback_query_handler(add_task_data, cb.filter(action=["change_channel", "change_description", "change_reward", "publish_task",
                                                                        "change_channel_id", "change_channel_link", "delete_task"]), state="*", user_id=admin_id)
    dp.register_message_handler(change_reward, state=Admin.AddTask.reward, user_id=admin_id)
    dp.register_message_handler(change_description, state=Admin.AddTask.description, user_id=admin_id)
    dp.register_message_handler(change_channel_id, state=Admin.AddTask.task_id, user_id=admin_id)
    dp.register_message_handler(get_task_id, state=Admin.DeleteTask.task_id, user_id=admin_id)