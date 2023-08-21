from utils.message_utils import text_editor
from aiogram import types, Dispatcher
from config.bot_data import admin_id
from config.bot_text import text
from markups import cb
import markups as nav


async def main_menu(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "admin_menu":
        await text_editor(text=text.admin_menu.format(name=call.from_user.first_name), call=call, markup=nav.admin_menu)

def register_handler_admin_main(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu, cb.filter(action=["admin_menu"]), user_id=admin_id)