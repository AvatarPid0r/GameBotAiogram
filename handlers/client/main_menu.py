import asyncio
import random

from aiogram.dispatcher import FSMContext

from config.bot_data import db, money_name, balance_for_click2, bot, balance_for_click1
from states.states import Client
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text, Text
from markups import cb
import markups as nav


async def click(user_id: int, call: types.CallbackQuery):
    msg = await text_editor(text=text.sleep_message, call=call)
    client_balance = (await db.get_client_date(user_id, ("balance",)))[0]
    m = random.randint(balance_for_click1, balance_for_click2)
    ma = await db.cheack_status(user_id=user_id)
    if ma == True:
        await db.update_data(user_id, ("balance", client_balance + m))
        await db.vikl_status(user_id=user_id)
        await sleep(5)
        await text_editor(text=text.pay_click.format(bal=m), call=call, message_id=msg.message_id, markup=nav.clicker_menu)

    else:
        await text_editor(text=text.pay_click_bad, call=call, message_id=msg.message_id, markup=nav.clicker_menu)

async def main_commands(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "profile" or call.data == 'profile':
        balance, username, waiters, chefs, market, admins, products = await asyncio.gather(
            db.get_client_date(call.from_user.id, ("balance",)),
            db.get_username_res(call.from_user.id),
            db.get_waiter(call.from_user.id),
            db.get_chefs(call.from_user.id),
            db.get_market(call.from_user.id),
            db.get_admins(call.from_user.id),
            db.get_products(call.from_user.id)
        )

        balance = balance[0]

        waiter1, waiter2, waiter3 = waiters
        all_waiter = waiter1 + waiter2 + waiter3

        chef1, chef2, chef3 = chefs
        all_chef = chef1 + chef2 + chef3

        promo, market, pr = market
        all_market = promo + market + pr

        admin_1, admin_2, admin_3 = admins
        all_admin = admin_1 + admin_2 + admin_3

        zakus, napitki, snack, desert, sklad, sklad_all, cheack_client = products

        sklad_all = sklad - sklad_all


        await text_editor(text=text.profile.format(
            ID=call.from_user.id,
            username=username,
            balance=round(balance, 1),
            referrer=await db.count_referrals(call.from_user.id),
            waiter=all_waiter,
            waiter1=waiter1,
            waiter2=waiter2,
            waiter3=waiter3,
            chef=all_chef,
            chef1=chef1,
            chef2=chef2,
            chef3=chef3,
            market=all_market,
            promo=promo,
            markets=market,
            pr=pr,
            admin=all_admin,
            admin_1=admin_1,
            admin_2=admin_2,
            admin_3=admin_3,
            zakus=zakus,
            desert=desert,
            napitki=napitki,
            snack=snack,
            sklad=sklad,
            sklad_all=sklad_all,
            cheack_client=cheack_client), call=call, markup=nav.my_res)
    elif action == "start":
        m = await db.check_res(user_id=call.from_user.id)
        if m:
            await text_editor(text=text.main_menu.format(money_name=money_name),
                              call=call,
                              markup=nav.main_menu(call.from_user.id))
        else:
            await text_editor(text=Text.create_name_res, call=call)
            await Client.Create_res.name.set()
    elif action == "start_earn":
        await text_editor(text=text.earn, call=call, markup=nav.earn_keyboard)
    elif action == "invite_friends":
        username = (await bot.get_me()).username
        await text_editor(text=text.invite.format(link=f"https://t.me/{username}?start={call.from_user.id}"),
                          call=call, markup=nav.back_button("earn_menu"))
    elif action == "clicker":
        await text_editor(text=text.clicker, call=call, markup=nav.clicker_menu)
    elif action == "click":
        create_task(click(call.from_user.id, call))
    elif action == "product":
        zakus, napitki, snack, desert, _, _, _ = await db.get_products(user_id=call.from_user.id)

        products = await db.get_products(call.from_user.id)

        zakus, napitki, snack, desert, sklad, sklad_all, cheack_client = products

        sklad_all = sklad - sklad_all

        await text_editor(text=text.product.format(zakus=zakus,
                                                   napitki=napitki,
                                                   snacks=snack,
                                                   desers=desert,
                                                   sklad=sklad,
                                                   sklad_all=sklad_all), call=call, markup=nav.product_keyboard)
    elif action == "personal":
        await text_editor(text=text.personal, call=call, markup=nav.personal_keyboard)
    elif action == "info":
        await text_editor(text=text.info, call=call, markup=nav.info_keyboard)


def register_handler_client_main(dp: Dispatcher):
    dp.register_callback_query_handler(main_commands, cb.filter(action=["profile", "start_earn", "start",
                                                                        "invite_friends", "clicker", "click", "product",
                                                                        "personal", "info", "vitrina_settings"]))
