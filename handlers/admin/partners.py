import os

from aiogram.dispatcher import FSMContext

from states.states import Admin
from utils.message_utils import text_editor
from aiogram import types, Dispatcher
from config.bot_data import admin_id, dp, db_json, bot
from config.bot_text import text
from markups import cb
import markups as nav
from utils.revenue_send_all import send_all


@dp.callback_query_handler(lambda x: x.data == 'create_partner')
async def create_partner(callback: types.CallbackQuery) -> None:
    await text_editor(text=text.create_partner, call=callback, markup=nav.back_button("admin_menu"))
    await Admin.AddPartner.name.set()


@dp.message_handler(state=Admin.AddPartner.name)
async def create_partner(message: types.Message, state: FSMContext):
    name = message.text
    m = await db_json.create_partner(name=name)
    if m == True:
        await text_editor(text=text.good_create_partner.format(partner=name), message=message, markup=nav.admin_menu)
    else:
        await text_editor(text=text.bad_create_partner.format(partner=name), message=message,
                          markup=nav.admin_menu)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'delete_partner')
async def create_partner(callback: types.CallbackQuery) -> None:
    await text_editor(text=text.del_partner, call=callback, markup=nav.back_button("admin_menu"))
    await Admin.AddPartner.del_name.set()


@dp.message_handler(state=Admin.AddPartner.del_name)
async def create_partner(message: types.Message, state: FSMContext) -> None:
    name = message.text
    m = await db_json.del_partner(name=name)
    if m == True:
        await text_editor(text=text.good_del_partner.format(partner=name), message=message, markup=nav.admin_menu)
    else:
        await text_editor(text=text.bad_del_partner.format(partner=name), message=message,
                          markup=nav.admin_menu)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'add_cert')
async def create_partner(callback: types.CallbackQuery) -> None:
    await text_editor(text=text.create_partner, call=callback, markup=nav.back_button("admin_menu"))
    await Admin.AddPartner.add_cert.set()


@dp.message_handler(state=Admin.AddPartner.add_cert)
async def create_partner(message: types.Message, state: FSMContext) -> None:
    m = await db_json.cheack_partner(name=message.text)
    if m == True:
        await state.update_data(partner=message.text)
        await text_editor(text=text.add_certificat, message=message, markup=nav.back_button("admin_menu"))
        await Admin.AddPartner.add_cert1.set()
    else:
        await text_editor(text=text.no_find_partner.format(partner=message.text), message=message,
                          markup=nav.admin_menu)
        await state.finish()


@dp.message_handler(state=Admin.AddPartner.add_cert1, content_types=[types.ContentType.DOCUMENT])
async def create_partner(message: types.Message, state: FSMContext) -> None:
    document = message.document
    file_name = document.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    await message.document.download(file_path)
    data = await state.get_data()
    name_partner = data.get('partner')
    good, error = await db_json.add_certificat(path_=file_path, name_partner=name_partner)
    await text_editor(text=text.good_add_cert.format(good=good[0], error=error[0]), message=message,
                      markup=nav.admin_menu)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'del_cert')
async def create_partner(callback: types.CallbackQuery) -> None:
    await text_editor(text=text.create_partner, call=callback, markup=nav.back_button("admin_menu"))
    await Admin.AddPartner.del_cert.set()


@dp.message_handler(state=Admin.AddPartner.del_cert)
async def create_partner(message: types.Message, state: FSMContext) -> None:
    m = await db_json.cheack_partner(name=message.text)
    if m == True:
        await state.update_data(partner=message.text)
        await text_editor(text=text.del_cert, message=message, markup=nav.back_button("admin_menu"))
        await Admin.AddPartner.del_cert1.set()
    else:
        await text_editor(text=text.no_find_partner.format(partner=message.text), message=message,
                          markup=nav.admin_menu)
        await state.finish()


@dp.message_handler(state=Admin.AddPartner.del_cert1)
async def create_partner(message: types.Message, state: FSMContext) -> None:
    name = message.text
    data = await state.get_data()
    name_partner = data.get('partner')
    m = await db_json.del_cert(name=name, name_partner=name_partner)
    if m == True:
        await text_editor(text=text.del_cert_good.format(partner=name_partner, name=name), message=message,
                          markup=nav.admin_menu)
    else:
        await text_editor(text=text.del_cert_bad.format(partner=name_partner, name=name), message=message,
                          markup=nav.admin_menu)

    await state.finish()
