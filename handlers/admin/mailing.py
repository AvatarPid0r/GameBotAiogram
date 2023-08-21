from config.bot_data import admin_id, db, bot
from utils.message_utils import text_editor
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from config.bot_text import text
from states.states import Admin
from markups import cb
import markups as nav
import asyncio

async def mailing_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "mailing_menu":
        await text_editor(text=text.mailing,
                          call=call,
                          markup=nav.back_button("admin_menu"))
        await Admin.Mailing.get_data.set()


async def get_mailing_data(message: types.Message, state: FSMContext):
    content = message.content_type
    async with state.proxy() as data:
        if content == "text":
            data["text"] = message.parse_entities()
        if content == "photo":
            data["file_id"] = message.photo[-1].file_id
            data["text"] = message.caption
    await bot.send_message(message.from_user.id, "➖" * 10)
    if content == "text":
        await bot.send_message(message.from_user.id, data["text"], parse_mode=types.ParseMode.HTML)
    elif content == "photo":
        await bot.send_photo(chat_id=message.from_user.id, photo=data["file_id"], caption=data["text"])
    await bot.send_message(message.from_user.id, "➖" * 10 + "\nЕсли вас все устраивает, нажмите подтвердить", reply_markup=nav.confirm_menu, parse_mode=types.ParseMode.HTML)
    await state.update_data(file_type=content, text=data.get("text"), file_id=data.get("file_id"))

async def send_loop(call: types.CallbackQuery, content: str, file_id: str, text: str):
    users = await db.get_all_client()
    user_id = call.from_user.id
    sent, not_sent = 0, 0
    for user in users:
        try:
            if content == "photo":
                await bot.send_photo(chat_id=user, photo=file_id, caption=text)
            elif content == "text":
                await bot.send_message(user, text, parse_mode=types.ParseMode.HTML)
            sent += 1
        except:
            not_sent += 1
        await asyncio.sleep(0.08)
    await bot.send_message(user_id, f"📥 Рассылка закончилась\n{'➖' * 10}\n🔔 - {sent}\n🔕 - {not_sent}\n{'➖' * 10}", reply_markup=nav.admin_menu)

async def send_message(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    content = data.get("file_type")
    file_id = data.get("file_id")
    text = data.get("text")
    asyncio.create_task(send_loop(call, content, file_id, text))
    await bot.send_message(call.from_user.id, "📤 Рассылка началась", reply_markup=nav.back_button("main_menu"))
    await state.finish()


def register_handler_admin_mailing(dp: Dispatcher):
    dp.register_callback_query_handler(mailing_menu, cb.filter(action=["mailing_menu"]), user_id=admin_id)
    dp.register_message_handler(get_mailing_data, state=Admin.Mailing.get_data, content_types=["text", "photo"], user_id=admin_id)
    dp.register_callback_query_handler(send_message, cb.filter(action=["confirm"]), state="*", user_id=admin_id)