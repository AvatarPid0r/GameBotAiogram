import json
import random
from datetime import datetime, date, timedelta
import aiosqlite
from typing import Union

from config.settings_res import *


class DataBase:
    def __init__(self, db_path: str):
        self._db_path = db_path

    async def db_request(self, query: str, param: tuple = (), fetchone: bool = False, fetchall: bool = False):
        async with aiosqlite.connect(self._db_path) as connection:
            async with connection.execute(query, param) as cursor:
                await connection.commit()
                if fetchone:
                    return await cursor.fetchone()
                elif fetchall:
                    return await cursor.fetchall()

    async def add_client(self, user_id: int, username: str, balance: int = balance, deals_day: int = 0,
                         personal_count: int = 0, courer_count: int = 0, safe_count: int = 0, logist_count: int = 0,
                         pr_count: int = 0, adm_count: int = 0, release_count: int = 0, stim_count: int = 0,
                         eiph_count: int = 0, mj_count: int = 0, med_count: int = 0, referrer_earn: int = 0,
                         status: int = 0):
        try:
            await self.db_request("INSERT INTO client VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                user_id, balance, datetime.now(), username, deals_day, personal_count, courer_count, safe_count,
                logist_count, pr_count, adm_count, release_count, stim_count, eiph_count, mj_count, med_count,
                referrer_earn, status))
        except aiosqlite.IntegrityError:
            pass

    async def add_referral(self, user_id: int, referrer_id: int = None) -> None:
        if referrer_id is not None:
            await self.db_request("INSERT INTO referral ('user_id', 'referrer_id') VALUES (?, ?)",
                                  (user_id, referrer_id,))
        else:
            await self.db_request("INSERT INTO referral ('user_id') VALUES (?)", (user_id,))

    async def client_exists(self, user_id: int, table: str = "client") -> bool:
        result = await self.db_request(f"SELECT * FROM {table} WHERE user_id = ?", (user_id,), fetchone=True)
        return bool(result)

    async def get_client_date(self, user_id: int, data: tuple) -> tuple:
        result = await self.db_request(f"SELECT {', '.join(data)} FROM client WHERE user_id = ?", (user_id,),
                                       fetchall=True)
        return result[0]

    async def update_data(self, user_id: int, data: tuple) -> None:
        await self.db_request(f"UPDATE client SET {data[0]} = ? WHERE user_id = ?", (data[1], user_id,)),

    async def deals_day(self, user_id: int) -> int:
        result = await self.db_request("SELECT COUNT(id) as count FROM client WHERE deals_day = ?", (user_id,),
                                       fetchone=True)
        return result[0]

    async def count_referrals(self, user_id: int) -> int:
        result = await self.db_request("SELECT COUNT(id) as count FROM referral WHERE referrer_id = ?", (user_id,),
                                       fetchone=True)
        return result[0]

    async def get_clients_reg_date(self) -> list:
        return [i[0] for i in await self.db_request("SELECT register_time FROM client", fetchall=True)]

    async def get_all_client(self) -> list:
        return [user_id[0] for user_id in await self.db_request("SELECT user_id FROM client", fetchall=True)]

    async def get_task_data(self, task_id: int = None, completed_tasks: list = None) -> dict:
        if task_id:
            result = await self.db_request("SELECT description, reward, channel_id FROM tasks WHERE task_id = ?",
                                           (task_id,), fetchall=True)
        else:
            result = await self.db_request("SELECT * FROM tasks", fetchall=True)
        if completed_tasks is not None:
            return {index: {"description": description, "reward": reward, "channel_id": channel_id} for
                    index, description, reward, channel_id in result if index not in completed_tasks}
        return {"description": result[0][0], "reward": result[0][1], "channel_id": result[0][2]}

    async def add_task(self, description: str, reward: int, channel_id: int = None):
        await self.db_request("INSERT INTO tasks (description, reward, channel_id) VALUES(?, ?, ?)",
                              (description, reward, channel_id,))

    async def task_exists(self, task_id: int) -> bool:
        result = await self.db_request("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,), fetchone=True)
        return bool(result)

    async def delete_task(self, task_id: int):
        async with aiosqlite.connect(self._db_path) as connection:
            await connection.execute("BEGIN")
            await connection.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            await connection.execute("DELETE FROM client_tasks WHERE task_id = ?", (task_id,))
            await connection.execute("UPDATE tasks SET task_id = task_id - 1 WHERE task_id > ?", (task_id,))
            await connection.commit()

    async def get_completed_tasks(self, user_id: int) -> list:
        result = await self.db_request("SELECT task_id FROM client_tasks WHERE user_id = ?", (user_id,), fetchall=True)
        return [i[0] for i in result]

    async def add_completed_task(self, user_id: int, task_id: int):
        try:
            await self.db_request("INSERT INTO client_tasks VALUES(?, ?)", (user_id, task_id,))
        except aiosqlite.IntegrityError:
            pass

    async def add_promo(self, promo: str, reward: int):
        try:
            await self.db_request("INSERT INTO promocodes VALUES(?, ?)", (promo, reward,))
        except aiosqlite.IntegrityError:
            pass

    async def promo_exists(self, promo: str) -> bool:
        result = await self.db_request("SELECT 1 FROM promocodes WHERE promo = ?", (promo,), fetchone=True)
        return bool(result)

    async def delete_promo(self, promo: str):
        await self.db_request("DELETE FROM promocodes WHERE promo = ?", (promo,))

    async def get_promo_reward(self, promo: str) -> int:
        result = await self.db_request("SELECT reward FROM promocodes WHERE promo = ?", (promo,), fetchone=True)
        return result[0]

    async def add_entered_promo(self, user_id: int, promo: str):
        try:
            await self.db_request("INSERT INTO client_promo VALUES (?, ?)", (user_id, promo,))
        except aiosqlite.IntegrityError:
            pass

    async def is_promo_used(self, user_id: int, promo: str) -> bool:
        result = await self.db_request("SELECT 1 FROM client_promo WHERE promo = ? and user_id = ?", (promo, user_id,),
                                       fetchone=True)
        return bool(result)

    async def get_username_res(self, user_id: int):
        result = await self.db_request('SELECT name_res FROM res_all WHERE user_id = ?', (user_id,), fetchone=True)

        return result[0]

    async def get_waiter(self, user_id: int):
        waiter1 = await self.db_request('SELECT waiter_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        waiter2 = await self.db_request('SELECT waiter_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        waiter3 = await self.db_request('SELECT waiter_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)

        return int(waiter1[0]), int(waiter2[0]), int(waiter3[0])

    async def get_chefs(self, user_id: int):
        chefs_1 = await self.db_request('SELECT chefs_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        chefs_2 = await self.db_request('SELECT chefs_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        chefs_3 = await self.db_request('SELECT chefs_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)

        return int(chefs_1[0]), int(chefs_2[0]), int(chefs_3[0])

    async def get_market(self, user_id: int):
        promo = await self.db_request('SELECT marketing_1 FROM res_staff WHERE user_id = ?', (user_id,),
                                      fetchone=True)
        market = await self.db_request('SELECT marketing_2 FROM res_staff WHERE user_id = ?', (user_id,),
                                       fetchone=True)
        pr = await self.db_request('SELECT marketing_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)

        return int(promo[0]), int(market[0]), int(pr[0])

    async def get_admins(self, user_id: int):
        admin_1 = await self.db_request('SELECT admin_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        admin_2 = await self.db_request('SELECT admin_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)
        admin_3 = await self.db_request('SELECT admin_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True)

        return int(admin_1[0]), int(admin_2[0]), int(admin_3[0])

    async def get_products(self, user_id: int):
        sklad = \
            (await self.db_request('SELECT sklad1 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[
                0] * vessklad_1 \
            + (await self.db_request('SELECT sklad2 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[
                0] * vessklad_2 \
            + (await self.db_request('SELECT sklad3 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[
                0] * vessklad_3
        sklad_all = await self.db_request(f'SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,),
                                          fetchone=True)
        zakus = await self.db_request('SELECT product1 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True)
        napitki = await self.db_request('SELECT product2 FROM res_products WHERE user_id = ?', (user_id,),
                                        fetchone=True)
        snack = await self.db_request('SELECT product3 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True)
        desert = await self.db_request('SELECT product4 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True)

        cheack_client = await self.db_request('SELECT client_all FROM res_all WHERE user_id = ?', (user_id,),
                                              fetchone=True)
        return int(zakus[0]), int(napitki[0]), int(snack[0]), int(desert[0]), int(sklad), int(sklad_all[0]), int(
            cheack_client[0])

    async def check_oficiant(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        sklad_all = (await self.db_request(f'SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,),
                                           fetchone=True))[0]
        if balance < globals()[f'buy_oficiant_{tip}']:
            return None
        elif sklad_all < globals()[f'limit_hiring_{tip}']:
            return None
        return True

    async def buy_ofic(self, user_id: int, tip: int):
        buy_oficiant_column = globals()[f'buy_oficiant_{tip}']
        balance = int(
            (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[
                0]) - buy_oficiant_column
        count = (await self.db_request(f'SELECT waiter_{tip} FROM res_staff WHERE user_id = ?', (user_id,),
                                       fetchone=True))[0]
        count += 1
        await self.db_request(f'UPDATE res_staff SET waiter_{tip} = ? WHERE user_id = ?', (count, user_id))
        await self.db_request(f'UPDATE client SET balance = ? WHERE user_id = ?', (balance, user_id))
        sklad_all = (await self.db_request(f'SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,),
                                           fetchone=True))[0]
        sklad_all -= globals()[f'limit_hiring_{tip}']
        await self.db_request(f'UPDATE res_products SET sklad_all = ? WHERE user_id = ?', (sklad_all, user_id))

    async def cheack_buy_sklad(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        if balance < globals()[f'buysklad_{tip}']:
            return None
        return True

    async def buy_sklad(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        balance -= globals()[f'buysklad_{tip}']
        vessklada = \
            (await self.db_request('SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[
                0]
        vessklada += globals()[f'vessklad_{tip}']
        count_sklad = \
            (await self.db_request(f'SELECT sklad{tip} FROM res_products WHERE user_id = ?', (user_id,),
                                   fetchone=True))[0]
        count_sklad += 1
        await self.db_request(f'UPDATE res_products SET sklad_all=?, sklad{tip}=? WHERE user_id = ?',
                              (vessklada, count_sklad, user_id))
        await self.db_request(f'UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))

    async def cheack_but_citchen(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        if balance < globals()[f'buycitchen_{tip}']:
            return None
        return True

    async def buy_citchen(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        balance -= globals()[f'buycitchen_{tip}']
        count_citchen = int(
            (await self.db_request(f'SELECT chefs_{tip} FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[
                0])
        count_citchen += 1
        await self.db_request(f'UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))
        await self.db_request(f'UPDATE res_staff SET chefs_{tip}=? WHERE user_id=?', (count_citchen, user_id))

    async def cheack_but_marketologa(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        if balance < globals()[f'buymarker_{tip}']:
            return None
        return True

    async def buy_marketologs(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        balance -= globals()[f'buymarker_{tip}']
        count_market = int((await self.db_request(f'SELECT marketing_{tip} FROM res_staff WHERE user_id = ?',
                                                  (user_id,), fetchone=True))[0])
        client_alls = \
            (await self.db_request('SELECT client_all FROM res_all WHERE user_id=?', (user_id,), fetchone=True))[0]

        if int(tip) == 1:
            client_alls += markpromo_1
        elif int(tip) == 2:
            client_alls += marketmarketolog_2
        elif int(tip) == 3:
            client_alls += marketpr_3

        await self.db_request('UPDATE res_all SET client_all=? WHERE user_id=?', (int(client_alls), user_id))
        count_market += 1

        await self.db_request(f'UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))
        await self.db_request(f'UPDATE res_staff SET marketing_{tip}=? WHERE user_id=?', (count_market, user_id))

    async def cheack_buy_administ(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        if balance < globals()[f'buyadmin_{tip}']:
            return None
        return True

    async def buy_admin(self, user_id: int, tip: int):
        balance = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        balance -= globals()[f'buyadmin_{tip}']
        count_admin = int((await self.db_request(f'SELECT admin_{tip} FROM res_staff WHERE user_id = ?',
                                                 (user_id,), fetchone=True))[0])
        count_admin += 1
        await self.db_request(f'UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))
        await self.db_request(f'UPDATE res_staff SET admin_{tip}=? WHERE user_id=?', (count_admin, user_id))

    async def check_purchase(self, user_id: int, product: int, count: int) -> str:
        balance: int = (
            await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True)
        )[0]
        sklad_all: int = (
            await self.db_request('SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,), fetchone=True)
        )[0]
        price: int = int(count) * int(globals()[f'buyproduct_{product}'])
        vesproduct: int = int(count) * int(globals()[f'vesproduct_{product}'])

        if int(price) > int(balance):
            return "❌ Недостаточно средств для покупки"

        elif int(count) < int(globals()[f'limitproduct_{product}']):
            return f"❌ Минимальное количество для покупки: {globals()[f'limitproduct_{product}']} единиц"

        elif int(sklad_all) < int(vesproduct):
            return "❌ Недостаточно места на складе"

        return ""

    async def buy_product(self, user_id: int, product: int, count: int) -> Union[str, bool]:
        check_result = await self.check_purchase(user_id, product, count)
        if check_result:
            return check_result

        count_product: int = (
            await self.db_request(f'SELECT product{product} FROM res_products WHERE user_id = ?', (user_id,),
                                  fetchone=True)
        )[0]
        count_product += int(count)
        balance: int = (
            await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True)
        )[0]
        sklad_all: int = (
            await self.db_request('SELECT sklad_all FROM res_products WHERE user_id = ?', (user_id,), fetchone=True)
        )[0]
        price: int = int(count) * int(globals()[f'buyproduct_{product}'])
        vesproduct: int = int(count) * int(globals()[f'vesproduct_{product}'])

        balance -= int(price)
        sklad_all -= int(vesproduct)

        await self.db_request(f'UPDATE res_products SET sklad_all=?, product{product}=? WHERE user_id = ?',
                              (sklad_all, count_product, user_id))
        await self.db_request('UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))

        return True

    async def create_res(self, user_id: int, name: str):
        sklad_all = (int(sklad_1) * int(vessklad_1)) + (int(sklad_2) * int(vessklad_2)) + (
                int(sklad_3) * int(vessklad_3))
        sklad_all -= (int(zakuski) * int(vesproduct_1)) + (int(napitki) * int(vesproduct_2)) + (
                int(snack) * int(vesproduct_3)) + (int(desert) * int(vesproduct_4))
        sklad_all -= (int(oficant_1) * int(limit_hiring_1)) + (int(oficant_2) * int(limit_hiring_2)) + (
                int(oficant_3) * int(limit_hiring_3))

        client_all = (int(marketing_promo) * int(markpromo_1)) + (int(marketing_market) * int(marketmarketolog_2)) + (
                int(marketing_pr) * int(marketpr_3)) + int(startup)

        await self.db_request('INSERT INTO res_all VALUES (?, ?, ?, ?, ?, ?)',
                              (
                                  user_id, name, balance, client_all, fart, 0
                              ))

        await self.db_request('UPDATE client SET balance=? WHERE user_id=?', (balance, user_id))

        await self.db_request('INSERT INTO res_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            user_id, sklad_all, sklad_1, sklad_2, sklad_3, zakuski, napitki, snack, desert
        ))
        await self.db_request('INSERT INTO res_staff VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            user_id, oficant_1, oficant_2, oficant_3, chefs_1, chefs_2, chefs_2, marketing_promo, marketing_market,
            marketing_pr, administator_1, administator_2, administator_3, 0, 0, 0, 1
        ))
        await self.db_request('INSERT INTO res_vitrina (user_id) VALUES (?)', (user_id,))
        await self.db_request('INSERT INTO res_improvement (user_id) VALUES (?)', (user_id,))

    async def check_res(self, user_id: int):
        result = await self.db_request('SELECT balance FROM res_all WHERE user_id = ?', (user_id,), fetchone=True)
        if result:
            return True
        else:
            return None

    async def change_sett(self, user_id: int, number: int, wai: int):
        await self.db_request(f'UPDATE res_vitrina SET settings_{wai}=? WHERE user_id=?', (number, user_id))

    async def cheack_sett(self, user_id: int):
        sett = []
        for i in range(1, 5):
            cheack = (await self.db_request(f'SELECT settings_{i} FROM res_vitrina WHERE user_id = ?', (user_id,),
                                            fetchone=True))[0]
            if cheack == 1:
                sett.append('✅')
                sett.append('❌')
                sett.append('❌')
                if i in [3, 4]:
                    sett.append('❌')
            elif cheack == 2:
                sett.append('❌')
                sett.append('✅')
                sett.append('❌')
                if i in [3, 4]:
                    sett.append('❌')
            elif cheack == 3:
                sett.append('❌')
                sett.append('❌')
                sett.append('✅')
                if i in [3, 4]:
                    sett.append('❌')
            elif cheack == 4:
                sett.append('❌')
                sett.append('❌')
                sett.append('❌')
                if i in [3, 4]:
                    sett.append('✅')

        return sett

    async def cheack_improvement(self, user_id: int):
        result = await (self.db_request(
            'SELECT improvement_1, improvement_2, improvement_3, improvement_4, improvement_5 FROM res_improvement WHERE user_id = ?',
            (user_id,), fetchone=True))
        improvement_1, improvement_2, improvement_3, improvement_4, improvement_5 = result
        return improvement_1, improvement_2, improvement_3, improvement_4, improvement_5

    async def buy_improvement(self, user_id: int, product: int):
        cheack = (
            await self.db_request(f'SELECT improvement_{product} FROM res_improvement WHERE user_id = ?', (user_id,),
                                  fetchone=True))[0]
        cheack_balance = \
            (await self.db_request(f'SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
        if cheack_balance < globals()[f'price_improvement_{product}']:
            return None
        cheack_balance -= globals()[f'price_improvement_{product}']
        cheack += 1
        await self.db_request(f'UPDATE client SET balance=? WHERE user_id=?', (cheack_balance, user_id))
        await self.db_request(f'UPDATE res_improvement SET improvement_{product}=? WHERE user_id=?', (cheack, user_id))

    async def check_improvement(self, user_id: int, product: int) -> bool:
        cheack_balance = \
            (await self.db_request(f'SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]

        if cheack_balance < globals()[f'price_improvement_{product}']:
            return False
        if int(product) == 4:
            cheack_waiter = (await self.db_request('SELECT waiter_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            cheack_waiter2 = (await self.db_request('SELECT waiter_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            if cheack_waiter == 0 and cheack_waiter2 == 0:
                return False
        return True


    async def review(self, user_id: int):
        count_oficant_1 = \
            (await self.db_request('SELECT waiter_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_oficant_2 = \
            (await self.db_request('SELECT waiter_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_oficant_3 = \
            (await self.db_request('SELECT waiter_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_product_1 = \
            (await self.db_request('SELECT product1 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_product_2 = \
            (await self.db_request('SELECT product2 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_product_3 = \
            (await self.db_request('SELECT product3 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_product_4 = \
            (await self.db_request('SELECT product4 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_admin = 0
        count_all_admin += \
            (await self.db_request('SELECT admin_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_admin += \
            (await self.db_request('SELECT admin_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_admin += \
            (await self.db_request('SELECT admin_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_market = 0
        count_all_market += \
            (await self.db_request('SELECT marketing_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_market += \
            (await self.db_request('SELECT marketing_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
        count_all_market += \
            (await self.db_request('SELECT marketing_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]

        settings_1 = \
            (await self.db_request('SELECT settings_1 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                0]
        settings_2 = \
            (await self.db_request('SELECT settings_2 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                0]
        settings_3 = \
            (await self.db_request('SELECT settings_3 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                0]
        settings_4 = \
            (await self.db_request('SELECT settings_4 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                0]

        if count_product_1 == 0:
            count_product_1 = False
        else:
            count_product_1 = True
        if count_product_2 == 0:
            count_product_2 = False
        else:
            count_product_2 = True
        if count_product_3 == 0:
            count_product_3 = False
        else:
            count_product_3 = True
        if count_product_4 == 0:
            count_product_4 = False
        else:
            count_product_4 = True
        if count_oficant_1 == 0:
            count_oficant_1 = False
        else:
            count_oficant_1 = True
        if count_oficant_2 == 0:
            count_oficant_2 = False
        else:
            count_oficant_2 = True
        if count_oficant_3 == 0:
            count_oficant_3 = False
        else:
            count_oficant_3 = True
        if count_all_admin == 0:
            count_all_admin = False
        else:
            count_all_admin = True
        if count_all_market == 0:
            count_all_market = False
        else:
            count_all_market = True

        if count_product_1 > 0 and count_product_2 > 0 and count_product_3 > 0 and count_product_4 > 0:
            result_product = True
        else:
            result_product = False

        return count_oficant_1, count_oficant_2, count_oficant_3, \
               count_all_admin, count_all_market, count_product_1, \
               count_product_2, count_product_3, count_product_4, \
               settings_1, settings_2, settings_3, settings_4, \
               result_product

    async def write_review(self, user_id: int, review: list):
        review_str = json.dumps(review, ensure_ascii=False)
        try:
            await self.db_request('INSERT INTO res_reporting (user_id, review) VALUES (?, ?)', (user_id, review_str))
        except:
            await self.db_request('UPDATE res_reporting SET review=? WHERE user_id=?', (review_str, user_id))

    async def read_review(self, user_id: int):
        result = await self.db_request('SELECT review FROM res_reporting WHERE user_id = ?', (user_id,), fetchone=True)
        if result is None:
            result = None
        else:
            result = result[0]

        return result

    async def cheack_status(self, user_id: int) -> bool:
        result = (await self.db_request('SELECT status FROM client WHERE user_id =?', (user_id,), fetchone=True))[0]
        if result == 0:
            return True
        else:
            return False

    async def vikl_status(self, user_id: int):
        await self.db_request('UPDATE client SET status = 1 WHERE user_id=?', (user_id,))

    async def res_revenue(self, user_id: int):
        global markpromo_1, marketmarketolog_2, marketpr_3
        try:
            market_1 = \
                (await self.db_request('SELECT marketing_1 FROM res_staff WHERE user_id=?', (user_id,), fetchone=True))[0]
            market_2 = \
                (await self.db_request('SELECT marketing_2 FROM res_staff WHERE user_id=?', (user_id,), fetchone=True))[0]
            market_3 = \
                (await self.db_request('SELECT marketing_3 FROM res_staff WHERE user_id=?', (user_id,), fetchone=True))[0]

            count_admin_1 = \
                (await self.db_request('SELECT admin_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_admin_2 = \
                (await self.db_request('SELECT admin_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_admin_3 = \
                (await self.db_request('SELECT admin_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]

            count_chefs_1 = \
                (await self.db_request('SELECT chefs_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_chefs_2 = \
                (await self.db_request('SELECT chefs_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_chefs_3 = \
                (await self.db_request('SELECT chefs_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]

            improvement_1 = (
                await self.db_request('SELECT improvement_1 FROM res_improvement WHERE user_id = ?', (user_id,),
                                      fetchone=True))[0]
            improvement_2 = (
                await self.db_request('SELECT improvement_2 FROM res_improvement WHERE user_id = ?', (user_id,),
                                      fetchone=True))[0]
            improvement_3 = (
                await self.db_request('SELECT improvement_3 FROM res_improvement WHERE user_id = ?', (user_id,),
                                      fetchone=True))[0]
            improvement_4 = (
                await self.db_request('SELECT improvement_4 FROM res_improvement WHERE user_id = ?', (user_id,),
                                      fetchone=True))[0]
            improvement_5 = (
                await self.db_request('SELECT improvement_5 FROM res_improvement WHERE user_id = ?', (user_id,),
                                      fetchone=True))[0]

            citc_del_1 = random.randint(0, 100)
            citc_del_2 = random.randint(0, 100)
            citc_del_3 = random.randint(0, 100)

            citc_del_status = 0

            if citchen_del_1 >= citc_del_1:
                count_chefs_1 = 0
                citc_del_status = 1
            if citchen_del_2 >= citc_del_2:
                count_chefs_2 = 0
                citc_del_status = 1
            if citchen_del_3 >= citc_del_3:
                count_chefs_3 = 0
                citc_del_status = 1

            del_1 = random.randint(0, 100)
            del_2 = random.randint(0, 100)
            del_3 = random.randint(0, 100)

            del_status = 0

            if oficant_1_del >= del_1:
                await self.db_request('UPDATE res_staff SET waiter_1 = MAX(waiter_1 - 1, 0) WHERE user_id = ?', (user_id,))
                del_status = 1
            if oficant_2_del >= del_2:
                await self.db_request('UPDATE res_staff SET waiter_2 = MAX(waiter_2 - 1, 0) WHERE user_id = ?', (user_id,))
                del_status = 1
            if oficant_3_del >= del_3:
                await self.db_request('UPDATE res_staff SET waiter_3 = MAX(waiter_3 - 1, 0) WHERE user_id = ?', (user_id,))
                del_status = 1

            count_oficant_1 = \
                (await self.db_request('SELECT waiter_1 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_oficant_2 = \
                (await self.db_request('SELECT waiter_2 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_oficant_3 = \
                (await self.db_request('SELECT waiter_3 FROM res_staff WHERE user_id = ?', (user_id,), fetchone=True))[0]

            count_product_1 = \
                (await self.db_request('SELECT product1 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_product_2 = \
                (await self.db_request('SELECT product2 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_product_3 = \
                (await self.db_request('SELECT product3 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            count_product_4 = \
                (await self.db_request('SELECT product4 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]

            settings_1 = \
                (await self.db_request('SELECT settings_1 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                    0]
            settings_2 = \
                (await self.db_request('SELECT settings_2 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                    0]
            settings_3 = \
                (await self.db_request('SELECT settings_3 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                    0]
            settings_4 = \
                (await self.db_request('SELECT settings_4 FROM res_vitrina WHERE user_id = ?', (user_id,), fetchone=True))[
                    0]

            plata_job_admin = (int(count_admin_1) * int(buy_sutki_admin_1)) + (
                    int(count_admin_2) * int(buy_sutki_admin_2)) + (int(count_admin_3) * int(buy_sutki_admin_3))
            plata_job_chefs = (int(count_chefs_1) * int(buy_sutki_citchen_1)) + (
                    int(count_chefs_2) * int(buy_sutki_citchen_2)) + (int(count_chefs_3) * int(buy_sutki_citchen_3))
            plata_job_market = (int(market_1) * int(buy_sutki_market_1)) + (int(market_2) * int(buy_sutki_market_2)) + (
                    int(market_3) * int(buy_sutki_market_3))

            fart_all = ((int(count_admin_1) * int(admin_1)) + (int(count_admin_2) * int(admin_2)) + (
                    int(count_admin_3) * int(admin_3)) + (improvement_5 * up_client_improvement_5)) / 100
            conflict = 0

            pribl = 0
            nopribl = 0
            upclient = 0
            downclient = 0
            if count_product_1 > 0 and count_product_2 > 0 and count_product_3 > 0 and count_product_4 > 0:
                pribl += procent_sell_all

            if settings_1 == 2:
                pribl += perelivat
                conflict += perelivat_conflict
            elif settings_1 == 3:
                nopribl += nedolivat
                conflict += nedolivat_conflict
            else:
                pass

            if settings_2 == 2:
                pribl += pricehigh
                conflict += pricehigh_otziv
            elif settings_2 == 3:
                nopribl += pricedown
                conflict += pricedown_otziv
            else:
                pass

            if settings_3 == 2:
                upclient += settings3_knopka1_1
                nopribl += settings3_knopka1_2
            elif settings_3 == 3:
                pribl += settings3_knopka2
            elif settings_3 == 4:
                downclient += settings3_knopka3_1
                pribl += settings3_knopka3_2
            else:
                pass

            if settings_4 == 4:
                upclient += settings4_knopka1_1
                conflict += settings4_knopka1_2
            elif settings_4 == 3:
                downclient += settings4_knopka2_1
                conflict += settings4_knopka2_2
            elif settings_4 == 2:
                conflict += settings4_knopka3
            else:
                pass
            client = (upclient + (upclient * fart_all)) + downclient
            pribls = (pribl + (pribl * fart_all) + nopribl) / 4
            all_oficiant = (count_oficant_1 * client_oficiant_1) + (count_oficant_2 * client_oficiant_2) + (
                    count_oficant_3 * client_oficiant_3)

            mark1_no = random.randint(0, 100)
            mark2_no = random.randint(0, 100)
            mark3_no = random.randint(0, 100)

            send_market = 0

            send_market_no = 0

            if nofart_1 >= mark1_no:
                market_1 = 0
                send_market_no = 1
            if nofart_2 >= mark2_no:
                market_2 = 0
                send_market_no = 1
            if nofart_3 >= mark3_no:
                market_3 = 0
                send_market_no = 1

            if yesfart_1 >= mark1_no:
                markpromo_1 = (markpromo_1 + (markpromo_1 * (yesfart_1_privod / 100)))
                send_market = 1
            if yesfart_2 >= mark2_no:
                marketmarketolog_2 = (marketmarketolog_2 + (marketmarketolog_2 * (yesfart_2_privod / 100)))
                send_market = 1
            if yesfart_3 >= mark3_no:
                marketpr_3 = (marketpr_3 + (marketpr_3 * (yesfart_3_privod / 100)))
                send_market = 1

            client_event = \
            (await self.db_request('SELECT event_client FROM res_all WHERE user_id = ?', (user_id,), fetchone=True))[0]

            all_clinet_ = (((market_1 * markpromo_1) + (market_2 * marketmarketolog_2) + (
                    market_3 * marketpr_3)) + startup) + (improvement_1 * up_client_improvement_1) + (
                                  improvement_2 * up_client_improvement_2) + (improvement_3 * up_client_improvement_3[0])
            all_clinet_ = all_clinet_ + (all_clinet_ * (int(client_event) / 100))
            await self.db_request('UPDATE res_all SET event_client = 0 WHERE user_id = ?', (user_id,))
            all_client = all_clinet_ + ((client / 100) * all_clinet_)

            if int(all_oficiant) >= int(all_client):
                all_client = all_client

            elif int(all_oficiant) < int(all_client):
                all_client = all_oficiant

            g_sell_product1 = int(
                all_client * (procent_sell_1 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
            g_sell_product2 = int(
                all_client * (procent_sell_2 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
            g_sell_product3 = int(
                all_client * (procent_sell_3 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
            g_sell_product4 = int(
                all_client * (procent_sell_4 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))

            if count_product_1 < g_sell_product1:
                g_sell_product1 = count_product_1

            if count_product_2 < g_sell_product2:
                g_sell_product2 = count_product_2

            if count_product_3 < g_sell_product3:
                g_sell_product3 = count_product_3

            if count_product_4 < g_sell_product4:
                g_sell_product4 = count_product_4

            otchet_1 = g_sell_product1
            otchet_2 = g_sell_product2
            otchet_3 = g_sell_product3
            otchet_4 = g_sell_product4

            money_product1 = int(g_sell_product1) * int(mapshaproduct_1)
            money_product2 = int(g_sell_product2) * int(mapshaproduct_2)
            money_product3 = int(g_sell_product3) * int(mapshaproduct_3)
            money_product4 = int(g_sell_product4) * int(mapshaproduct_4)

            money_product1 += (int(pribls) / 100) * money_product1
            money_product2 += (int(pribls) / 100) * money_product2
            money_product3 += (int(pribls) / 100) * money_product3
            money_product4 += (int(pribls) / 100) * money_product4
            all_balance = (int(money_product1) + int(money_product2) + int(money_product3) + int(money_product4))

            count_product_1 = max(g_sell_product1, 0)
            count_product_2 = max(g_sell_product2, 0)
            count_product_3 = max(g_sell_product3, 0)
            count_product_4 = max(g_sell_product4, 0)

            all_sell_product = count_product_1 + count_product_2 + count_product_3 + count_product_4

            if all_sell_product < all_client:
                all_client = all_sell_product

            all_client_oficiant = all_client

            procent_oficiant3 = min(count_oficant_3, all_client_oficiant // client_oficiant_3)
            procent_oficiant2 = 0
            procent_oficiant1 = 0
            alls = all_client_oficiant
            alls = max(alls - (procent_oficiant3 * client_oficiant_3), 0)
            if alls != 0:
                procent_oficiant2 = min(count_oficant_2, alls // client_oficiant_2)
                alls = max(alls - (procent_oficiant2 * client_oficiant_2), 0)
                if alls != 0:
                    procent_oficiant1 = min(count_oficant_1, alls // client_oficiant_1)
                    alls = max(alls - (procent_oficiant1 * client_oficiant_1), 0)

            plata_job_oficiant = (procent_oficiant3 * buy_sutki_oficiant_3) + (procent_oficiant2 * buy_sutki_oficiant_2) + (
                    procent_oficiant1 * buy_sutki_oficiant_1)

            add_desert = count_chefs_3 * citchen_1
            add_napitki = count_chefs_2 * citchen_2
            add_zakus_snack = count_chefs_1 * citchen_3

            citchen_up_produc_1 = random.randint(0, 100)
            citchen_up_produc_2 = random.randint(0, 100)
            citchen_up_produc_3 = random.randint(0, 100)

            citchen_up_produc_status = 0

            if citchen_up_1_pr >= citchen_up_produc_1:
                add_desert = add_desert + (add_desert * (citchen_up_1_pr / 100))
                citchen_up_produc_status = 1
            if citchen_up_2_pr >= citchen_up_produc_2:
                add_napitki = add_napitki + (add_napitki * (citchen_up_2_pr / 100))
                citchen_up_produc_status = 1
            if citchen_up_3_pr >= citchen_up_produc_3:
                add_zakus_snack = add_zakus_snack + (add_zakus_snack * (citchen_up_3_pr / 100))
                citchen_up_produc_status = 1

            dels_product_1 = \
                (await self.db_request('SELECT product1 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            dels_product_2 = \
                (await self.db_request('SELECT product2 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            dels_product_3 = \
                (await self.db_request('SELECT product3 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]
            dels_product_4 = \
                (await self.db_request('SELECT product4 FROM res_products WHERE user_id = ?', (user_id,), fetchone=True))[0]

            vesproduct1 = 0
            vesproduct2 = 0
            vesproduct3 = 0
            vesproduct4 = 0

            sklad_procent_1 = random.randint(0, 100)
            sklad_procent_2 = random.randint(0, 100)
            sklad_procent_3 = random.randint(0, 100)

            sk_status = 0

            if del_product_1 >= sklad_procent_1:
                vesproduct1 = dels_product_1 * vesproduct_1
                vesproduct1 = min(vesproduct1, vessklad_1)
                sk_status = 1
                if vessklad_1 > vesproduct1:
                    vesproduct2 = dels_product_2 * vesproduct_2
                    vesproduct2 = min(vesproduct2, vessklad_1 - vesproduct1)
                    vesproduct2s = vesproduct1 + vesproduct2
                    sk_status = 1
                    if vessklad_1 > vesproduct2s:
                        vesproduct3 = dels_product_3 * vesproduct_3
                        vesproduct3 = min(vesproduct3, vessklad_1 - vesproduct2s)
                        vesproduct3s = vesproduct2 + vesproduct3
                        sk_status = 1
                        if vessklad_1 > vesproduct3s:
                            vesproduct4 = dels_product_4 * vesproduct_4
                            vesproduct4 = min(vesproduct4, vessklad_1 - vesproduct3s)
                            sk_status = 1

            if del_product_2 >= sklad_procent_2:
                vesproduct1 = dels_product_1 * vesproduct_1
                vesproduct1 = min(vesproduct1, vessklad_2)
                sk_status = 1
                if vessklad_2 > vesproduct1:
                    vesproduct2 = dels_product_2 * vesproduct_2
                    vesproduct2 = min(vesproduct2, vessklad_2 - vesproduct1)
                    vesproduct2s = vesproduct1 + vesproduct2
                    sk_status = 1
                    if vessklad_2 > vesproduct2s:
                        vesproduct3 = dels_product_3 * vesproduct_3
                        vesproduct3 = min(vesproduct3, vessklad_2 - vesproduct2s)
                        vesproduct3s = vesproduct2 + vesproduct3
                        sk_status = 1
                        if vessklad_2 > vesproduct3s:
                            vesproduct4 = dels_product_4 * vesproduct_4
                            vesproduct4 = min(vesproduct4, vessklad_2 - vesproduct3s)
                            sk_status = 1

            if del_product_3 >= sklad_procent_3:
                vesproduct1 = dels_product_1 * vesproduct_1
                vesproduct1 = min(vesproduct1, vessklad_3)
                sk_status = 1
                if vessklad_3 > vesproduct1:
                    vesproduct2 = dels_product_2 * vesproduct_2
                    vesproduct2 = min(vesproduct2, vessklad_3 - vesproduct1)
                    vesproduct2s = vesproduct1 + vesproduct2
                    sk_status = 1
                    if vessklad_3 > vesproduct2s:
                        vesproduct3 = dels_product_3 * vesproduct_3
                        vesproduct3 = min(vesproduct3, vessklad_3 - vesproduct2s)
                        vesproduct3s = vesproduct2 + vesproduct3
                        sk_status = 1
                        if vessklad_3 > vesproduct3s:
                            vesproduct4 = dels_product_4 * vesproduct_4
                            vesproduct4 = min(vesproduct4, vessklad_3 - vesproduct3s)
                            sk_status = 1

            sg_1 = vesproduct1 // vesproduct_1
            sg_2 = vesproduct2 // vesproduct_2
            sg_3 = vesproduct3 // vesproduct_3
            sg_4 = vesproduct4 // vesproduct_4

            if sk_status == 1:
                all_ves = vesproduct1 + vesproduct2 + vesproduct3 + vesproduct4
                await self.db_request('UPDATE res_products SET sklad_all = sklad_all + ? WHERE user_id = ?',
                                      (all_ves, user_id))

            await self.db_request('UPDATE res_products SET product1 = MAX(product1 - ?, 0) WHERE user_id = ?',
                                  (sg_1, user_id))
            await self.db_request('UPDATE res_products SET product2 = MAX(product2 - ?, 0) WHERE user_id = ?',
                                  (sg_2, user_id))
            await self.db_request('UPDATE res_products SET product3 = MAX(product3 - ?, 0) WHERE user_id = ?',
                                  (sg_3, user_id))
            await self.db_request('UPDATE res_products SET product4 = MAX(product4 - ?, 0) WHERE user_id = ?',
                                  (sg_4, user_id))

            await self.db_request('UPDATE res_products SET product1 = MAX(product1 - ?, 0) WHERE user_id = ?',
                                  (g_sell_product1, user_id))
            await self.db_request('UPDATE res_products SET product2 = MAX(product2 - ?, 0) WHERE user_id = ?',
                                  (g_sell_product2, user_id))
            await self.db_request('UPDATE res_products SET product3 = MAX(product3 - ?, 0) WHERE user_id = ?',
                                  (g_sell_product3, user_id))
            await self.db_request('UPDATE res_products SET product4 = MAX(product4 - ?, 0) WHERE user_id = ?',
                                  (g_sell_product4, user_id))

            await self.db_request('UPDATE res_products SET product1 = product1 + ? WHERE user_id = ?',
                                  (add_zakus_snack, user_id))
            await self.db_request('UPDATE res_products SET product2 = product2 + ? WHERE user_id = ?',
                                  (add_napitki, user_id))
            await self.db_request('UPDATE res_products SET product3 = product3 + ? WHERE user_id = ?',
                                  (add_zakus_snack, user_id))
            await self.db_request('UPDATE res_products SET product4 = product4 + ? WHERE user_id = ?',
                                  (add_desert, user_id))

            g_sell_product1 *= int(vesproduct_1)
            g_sell_product2 *= int(vesproduct_2)
            g_sell_product3 *= int(vesproduct_3)
            g_sell_product4 *= int(vesproduct_4)

            count_product_s_1 = int(g_sell_product1) + add_zakus_snack
            count_product_s_2 = int(g_sell_product2) + add_napitki
            count_product_s_3 = int(g_sell_product3) + add_zakus_snack
            count_product_s_4 = int(g_sell_product4) + add_desert

            sklad_all = int(count_product_s_1 + count_product_s_2 + count_product_s_3 + count_product_s_4)

            conflict += ((int(count_oficant_1) * int(fart_oficant_1)) + (int(count_oficant_2) * int(fart_oficant_2)) + (
                    int(count_oficant_3) * int(fart_oficant_3)))
            conflict += defolt_conflict
            conflict -= (conflict * (fart_all))
            conflict -= (conflict * (improvement_3 * up_client_improvement_3[1]) / 100)
            count_conflict = conflict * ((all_client / 100))
            count_conflict = max(count_conflict, 0)
            money_conflict = count_conflict * random.randint(mini_conflict, max_conflict)

            adm_cosak_1 = random.randint(0, 100)
            adm_cosak_1_fart = random.randint(0, 100)
            adm_cosak_2 = random.randint(0, 100)
            adm_cosak_2_fart = random.randint(0, 100)
            adm_cosak_3 = random.randint(0, 100)
            adm_cosak_3_fart = random.randint(0, 100)

            admin_send = 0

            if admin_cosak_1 >= adm_cosak_1:
                money_conflict = money_conflict + (money_conflict * (admin_cosak_procent_1 / 100))
                admin_send = 1
            elif admin_fart_1 >= adm_cosak_1_fart:
                money_conflict = money_conflict - (money_conflict * (admin_fart_up_1 / 100))
                admin_send = 2

            if admin_cosak_2 >= adm_cosak_2:
                money_conflict = money_conflict + (money_conflict * (admin_cosak_procent_2 / 100))
                admin_send = 1
            elif admin_fart_2 >= adm_cosak_2_fart:
                money_conflict = money_conflict - (money_conflict * (admin_fart_up_2 / 100))
                admin_send = 2

            if admin_cosak_3 >= adm_cosak_3:
                money_conflict = money_conflict + (money_conflict * (admin_cosak_procent_3 / 100))
                admin_send = 1
            elif admin_fart_3 >= adm_cosak_3_fart:
                money_conflict = money_conflict - (money_conflict * (admin_fart_up_3 / 100))
                admin_send = 2

            await self.db_request('UPDATE res_products SET sklad_all = MAX(sklad_all - ?, 0) WHERE user_id = ?',
                                  (sklad_all, user_id))

            await self.db_request('UPDATE client SET status = 0 WHERE user_id=?', (user_id,))
            referal = await self.db_request('SELECT user_id FROM referral WHERE referrer_id = ?', (user_id,), fetchall=True)
            money = 0
            for i in referal:
                if user_id == i:
                    continue
                try:
                    i = i[0]
                    market_1_referall = \
                        (await self.db_request('SELECT marketing_1 FROM res_staff WHERE user_id=?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    market_2_referall = \
                        (await self.db_request('SELECT marketing_2 FROM res_staff WHERE user_id=?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    market_3_referall = \
                        (await self.db_request('SELECT marketing_3 FROM res_staff WHERE user_id=?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_oficant_1_referall = \
                        (await self.db_request('SELECT waiter_1 FROM res_staff WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_oficant_2_referall = \
                        (await self.db_request('SELECT waiter_2 FROM res_staff WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_oficant_3_referall = \
                        (await self.db_request('SELECT waiter_3 FROM res_staff WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_product_1_referall = \
                        (await self.db_request('SELECT product1 FROM res_products WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_product_2_referall = \
                        (await self.db_request('SELECT product2 FROM res_products WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_product_3_referall = \
                        (await self.db_request('SELECT product3 FROM res_products WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_product_4_referall = \
                        (await self.db_request('SELECT product4 FROM res_products WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    settings_1_referall = \
                        (await self.db_request('SELECT settings_1 FROM res_vitrina WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    settings_2_referall = \
                        (await self.db_request('SELECT settings_2 FROM res_vitrina WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    settings_3_referall = \
                        (await self.db_request('SELECT settings_3 FROM res_vitrina WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    settings_4_referall = \
                        (await self.db_request('SELECT settings_4 FROM res_vitrina WHERE user_id = ?', (int(i),),
                                               fetchone=True))[
                            0] or 0
                    count_admin_1_referall = \
                        (await self.db_request('SELECT admin_1 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]
                    count_admin_2_referall = \
                        (await self.db_request('SELECT admin_2 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]
                    count_admin_3_referall = \
                        (await self.db_request('SELECT admin_3 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]

                    count_chefs_1_referall = \
                        (await self.db_request('SELECT chefs_1 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]
                    count_chefs_2_referall = \
                        (await self.db_request('SELECT chefs_2 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]
                    count_chefs_3_referall = \
                        (await self.db_request('SELECT chefs_3 FROM res_staff WHERE user_id = ?', (user_id,),
                                               fetchone=True))[0]

                    pribl_referall = 0
                    nopribl_referall = 0
                    upclient_referall = 0
                    downclient_referall = 0
                    if count_product_1 > 0 and count_product_2 > 0 and count_product_3 > 0 and count_product_4 > 0:
                        pribl_referall += procent_sell_all

                    if settings_1_referall == 2:
                        pribl_referall += perelivat
                    elif settings_1_referall == 3:
                        nopribl_referall += nedolivat
                    else:
                        pass

                    if settings_2_referall == 2:
                        pribl_referall += pricehigh
                    elif settings_2_referall == 3:
                        nopribl_referall += pricedown
                    else:
                        pass

                    if settings_3_referall == 2:
                        upclient_referall += settings3_knopka1_1
                        nopribl_referall += settings3_knopka1_2
                    elif settings_3_referall == 3:
                        pribl_referall += settings3_knopka2
                    elif settings_3_referall == 4:
                        downclient_referall += settings3_knopka3_1
                        pribl_referall += settings3_knopka3_2
                    else:
                        pass

                    if settings_4_referall == 2:
                        upclient_referall += settings4_knopka1_1
                    elif settings_4_referall == 3:
                        downclient_referall += settings4_knopka2_1
                    else:
                        pass

                    plata_job_admin_referall = (int(count_admin_1_referall) * int(buy_sutki_admin_1)) + (
                            int(count_admin_2_referall) * int(buy_sutki_admin_2)) + (
                                                       int(count_admin_3_referall) * int(buy_sutki_admin_3))
                    plata_job_oficiant_referall = (int(count_oficant_1_referall) * int(buy_sutki_oficiant_1)) + (
                            int(count_oficant_2_referall) * int(buy_sutki_oficiant_2)) + (
                                                          int(count_oficant_3_referall) * int(buy_sutki_oficiant_3))
                    plata_job_chefs_referall = (int(count_chefs_1_referall) * int(buy_sutki_citchen_1)) + (
                            int(count_chefs_2_referall) * int(buy_sutki_citchen_2)) + (
                                                       int(count_chefs_3_referall) * int(buy_sutki_citchen_3))
                    plata_job_market_referall = (int(market_1_referall) + int(buy_sutki_market_1)) + (
                            int(market_2_referall) + int(buy_sutki_market_2)) + (
                                                        int(market_3_referall) + int(buy_sutki_market_3))

                    fart_all_referall = ((int(count_admin_1_referall) * int(admin_1)) + (
                            int(count_admin_2_referall) * int(admin_2)) + (
                                                 int(count_admin_3_referall) * int(admin_3))) / 100

                    client_referall = (upclient_referall + (upclient_referall * fart_all_referall)) + downclient_referall
                    pribls_referall = (pribl_referall + (pribl_referall * fart_all_referall) + nopribl_referall) / 4

                    all_oficiant_referall = (count_oficant_1_referall * client_oficiant_1) + (
                            count_oficant_2_referall * client_oficiant_2) + (
                                                    count_oficant_3_referall * client_oficiant_3)
                    all_clinet__referall = (
                            ((market_1_referall * markpromo_1) + (market_2_referall * marketmarketolog_2) + (
                                    market_3_referall * marketpr_3)) + startup)
                    all_client_referall = all_clinet__referall + ((client_referall / 100) * all_clinet__referall)

                    if int(all_oficiant_referall) > int(all_client_referall):
                        all_client_referall = all_client_referall
                    elif int(all_oficiant_referall) < int(all_client_referall):
                        all_client_referall = all_oficiant_referall

                    g_sell_product1_referall = int(
                        all_client_referall * (
                                procent_sell_1 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
                    g_sell_product2_referall = int(
                        all_client_referall * (
                                procent_sell_2 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
                    g_sell_product3_referall = int(
                        all_client_referall * (
                                procent_sell_3 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))
                    g_sell_product4_referall = int(
                        all_client_referall * (
                                procent_sell_4 / (procent_sell_1 + procent_sell_2 + procent_sell_3 + procent_sell_4)))

                    if count_product_1_referall < g_sell_product1_referall:
                        g_sell_product1_referall = count_product_1_referall

                    if count_product_2_referall < g_sell_product2_referall:
                        g_sell_product2_referall = count_product_2_referall

                    if count_product_3_referall < g_sell_product3_referall:
                        g_sell_product3_referall = count_product_3_referall

                    if count_product_4_referall < g_sell_product4_referall:
                        g_sell_product4_referall = count_product_4_referall

                    money_product1_referall = int(g_sell_product1_referall) * int(mapshaproduct_1)
                    money_product2_referall = int(g_sell_product2_referall) * int(mapshaproduct_2)
                    money_product3_referall = int(g_sell_product3_referall) * int(mapshaproduct_3)
                    money_product4_referall = int(g_sell_product4_referall) * int(mapshaproduct_4)
                    money_product1_referall += (int(pribls_referall) / 100) * money_product1_referall
                    money_product2_referall += (int(pribls_referall) / 100) * money_product2_referall
                    money_product3_referall += (int(pribls_referall) / 100) * money_product3_referall
                    money_product4_referall += (int(pribls_referall) / 100) * money_product4_referall

                    all_balance_referall = (int(money_product1_referall) + int(money_product2_referall) + int(
                        money_product3_referall) + int(money_product4_referall))
                    money += procent_to_referal * (all_balance_referall - (
                            plata_job_admin_referall + plata_job_chefs_referall + plata_job_market_referall + plata_job_oficiant_referall))
                    money = max(money, 0)
                except Exception as e:
                    pass

            await self.db_request('UPDATE res_improvement SET improvement_2 = MAX(improvement_2 - 1, 0) WHERE user_id = ?',
                                  (user_id,))
            await self.db_request('UPDATE res_improvement SET improvement_3 = MAX(improvement_3 - 1, 0) WHERE user_id = ?',
                                  (user_id,))
            await self.db_request('UPDATE res_improvement SET improvement_5 = MAX(improvement_5 - 1, 0) WHERE user_id = ?',
                                  (user_id,))

            clear_money = int(
                all_balance - (plata_job_admin + plata_job_chefs + plata_job_market + plata_job_oficiant) + int(
                    money) - int(money_conflict))

            day = date.today().strftime("%Y-%m-%d")
            week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
            week_end = (datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime("%Y-%m-%d")
            month = date.today().strftime("%Y-%m")

            try:
                clear_money = max(clear_money, 0)
                await self.db_request('INSERT INTO top VALUES (?, ?, ?, ?, ?, ?, ?)',
                                      (user_id, clear_money, day, clear_money, week_start, clear_money, month))
            except Exception as e:
                cheack_day = \
                    (await self.db_request('SELECT top_day_date FROM top WHERE user_id = ?', (user_id,), fetchone=True))[0]
                if cheack_day == day:
                    await self.db_request('UPDATE top SET top_day = MAX(top_day + ?, 0) WHERE user_id = ?',
                                          (clear_money, user_id))
                else:
                    await self.db_request('UPDATE top SET top_day = MAX(?, 0), top_day_date = ? WHERE user_id = ?',
                                          (clear_money, day, user_id))
                cheack_week = \
                    (await self.db_request('SELECT top_week_date FROM top WHERE user_id = ?', (user_id,), fetchone=True))[0]
                if cheack_week >= week_start and cheack_week <= week_end:
                    await self.db_request('UPDATE top SET top_week = MAX(top_week + ?, 0) WHERE user_id = ?',
                                          (clear_money, user_id))
                else:
                    await self.db_request('UPDATE top SET top_week = MAX(?, 0), top_week_date = ? WHERE user_id = ?',
                                          (clear_money, week_start, user_id))

                cheack_month = \
                    (await self.db_request('SELECT top_month_date FROM top WHERE user_id = ?', (user_id,), fetchone=True))[
                        0]
                if cheack_month == month:
                    await self.db_request('UPDATE top SET top_month = MAX(top_month + ?, 0) WHERE user_id = ?',
                                          (clear_money, user_id))
                else:
                    await self.db_request('UPDATE top SET top_month = MAX(?, 0), top_month_date = ? WHERE user_id = ?',
                                          (clear_money, month, user_id))

            result = {'all_client': int(all_clinet_),
                      'all_client_yes': int(all_client),
                      'all_sell_product': int(otchet_1) + int(otchet_2) + int(otchet_3) + int(
                          otchet_4),
                      'all_balance': (int(all_balance - (
                              plata_job_admin + plata_job_chefs + plata_job_market + plata_job_oficiant)) + int(
                          money)) - int(money_conflict),
                      'zakus': otchet_1,
                      'napitki': otchet_2,
                      'skacs': otchet_3,
                      'deserts': otchet_4,
                      'zakus_money': money_product1,
                      'napitki_money': money_product2,
                      'snacks_money': money_product3,
                      'deserts_money': money_product4,
                      'referall_money': int(money),
                      'plata_job_oficiant': plata_job_oficiant,
                      'plata_job_market': plata_job_market,
                      'plata_job_chefs': plata_job_chefs,
                      'plata_job_admin': plata_job_admin,
                      'count_conflict': int(count_conflict),
                      'money_conflict': int(money_conflict),
                      'shefs_no_product': citc_del_status,
                      'del_oficiant': del_status,
                      'no_market_client': send_market_no,
                      'market_client': send_market,
                      'up_product_citchen': citchen_up_produc_status,
                      'del_product_sklad': sk_status,
                      'admin_fart': admin_send}

            await self.db_request('UPDATE res_all SET client_all = ? WHERE user_id = ?', (all_client, user_id))

            try:
                await self.db_request(
                    'INSERT INTO res_reporting (user_id, conflict_money, conflict_count) VALUES (?, ?, ?)',
                    (user_id, int(money_conflict), int(count_conflict)))
            except:
                await self.db_request('UPDATE res_reporting SET conflict_money=?, conflict_count=? WHERE user_id = ?',
                                      (int(money_conflict), int(count_conflict), user_id))

            balancer = (await self.db_request('SELECT balance FROM client WHERE user_id = ?', (user_id,), fetchone=True))[0]
            write = balancer + (int(all_balance) + int(money) - int(money_conflict) - (
                    plata_job_admin + plata_job_chefs + plata_job_market + plata_job_oficiant))
            write = max(write, 0)
            await self.db_request('UPDATE client SET balance = ? WHERE user_id = ?',
                                  (int(write), user_id))

            return result
        except:
            pass

    async def cheack_all(self):
        result = await self.db_request('SELECT user_id FROM res_all', fetchall=True)
        return result

    async def cheack_otziv_conflict(self, user_id: int):
        result = (await self.db_request('SELECT conflict_money, conflict_count FROM res_reporting WHERE user_id=?',
                                        (user_id,), fetchall=True))[0]
        return result

    async def cheack_balance(self, user_id: int, price: int) -> bool:
        cheack = (await self.db_request('SELECT balance FROM client WHERE user_id=?', (user_id,), fetchone=True))[0]
        if int(price) >= int(cheack):
            return False
        return True

    async def buy_promocode(self, user_id: int, price: int):
        cheack = (await self.db_request('SELECT balance FROM client WHERE user_id=?', (user_id,), fetchone=True))[0]
        cheack -= int(price)
        await self.db_request('UPDATE client SET balance = ? WHERE user_id=?', (int(cheack), (user_id)))

    async def minus_balance(self, user_id: int, price: int):
        await self.db_request('UPDATE client SET balance = balance - ? WHERE user_id = ?', (int(price), user_id))

    async def get_top(self, privod: str, limit: int = limit_top):
        day = date.today().strftime("%Y-%m-%d")
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        week_end = (datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime("%Y-%m-%d")
        month = date.today().strftime("%Y-%m")
        if privod == 'day':
            result = await self.db_request(
                'SELECT r.name_res, t.top_day FROM top t JOIN res_all r ON t.user_id = r.user_id JOIN client c ON t.user_id = c.user_id WHERE t.top_day_date = ? ORDER BY t.top_day DESC LIMIT ?',
                (day, limit_top), fetchall=True)
            return result

        elif privod == 'week':
            result = await self.db_request(
                'SELECT r.name_res, t.top_week FROM top t JOIN res_all r ON t.user_id = r.user_id JOIN client c ON t.user_id = c.user_id WHERE t.top_week_date >= ? AND t.top_week_date <= ? ORDER BY t.top_week DESC LIMIT ?',
                (week_start, week_end, limit_top), fetchall=True)
            return result

        elif privod == 'month':
            result = await self.db_request(
                'SELECT c.username, t.top_month FROM top t JOIN client c ON t.user_id = c.user_id WHERE t.top_month_date = ? ORDER BY t.top_month DESC LIMIT ?',
                (month, limit_top), fetchall=True)
            return result

    async def create_event(self, event: str, text: str):
        if event == 'up_client':
            try:
                if int(text):
                    await self.db_request('UPDATE event SET client = ?', (text,))
                    await self.db_request('UPDATE event SET status = ?', (1,))
            except:
                return f'\n\n<b>❌ Значение <i>"{text}"</i> не может быть добавлено так как не является числовым форматом</b>'
        elif event == 'event_balance':
            try:
                if int(text):
                    await self.db_request('UPDATE event SET balance = ?', (text,))
                    await self.db_request('UPDATE event SET status = ?', (1,))
            except:
                return f'\n\n<b>❌ Значение <i>"{text}"</i> не может быть добавлено так как не является числовым форматом</b>'
        elif event == 'fart_event':
            if not text.isdigit():
                return '\n\n<b>❌Шанс не может быть отрицательным или содержать буквы</b>'
            await self.db_request('UPDATE event SET fart = ?', (text,))
            await self.db_request('UPDATE event SET status = ?', (1,))
        elif event == 'event_yes':
            await self.db_request('UPDATE event SET fart_text = ?', (text,))
            await self.db_request('UPDATE event SET status = ?', (1,))
        elif event == 'event_no':
            await self.db_request('UPDATE event SET no_fart_text = ?', (text,))
            await self.db_request('UPDATE event SET status = ?', (1,))
        return True

    async def cheack_event(self):
        client = await self.db_request('SELECT client FROM event', fetchone=True)
        balance = await self.db_request('SELECT balance FROM event', fetchone=True)
        fart = await self.db_request('SELECT fart FROM event', fetchone=True)
        fart_text = await self.db_request('SELECT fart_text FROM event', fetchone=True)
        fart_no_text = await self.db_request('SELECT no_fart_text FROM event', fetchone=True)
        status = await self.db_request('SELECT status FROM event', fetchone=True)
        return client[0], balance[0], fart[0], fart_text[0], fart_no_text[0], status[0]

    async def event_save(self, balance: int, client: int, user_id: int):
        await self.db_request('UPDATE client SET balance = balance + ? WHERE user_id = ?', (balance, user_id))
        await self.db_request('UPDATE res_all SET event_client = ? WHERE user_id = ?', (client, user_id))

    async def cheack_cithcen_work(self, user_id: int):
        citchen1 = \
        (await self.db_request('SELECT chefs_status_1 FROM res_staff WHERE user_id =?', (user_id,), fetchone=True))[0]
        citchen2 = \
        (await self.db_request('SELECT chefs_status_2 FROM res_staff WHERE user_id =?', (user_id,), fetchone=True))[0]
        citchen3 = \
        (await self.db_request('SELECT chefs_status_3 FROM res_staff WHERE user_id =?', (user_id,), fetchone=True))[0]
        citchen_status = \
        (await self.db_request('SELECT chefs_status_date FROM res_staff WHERE user_id =?', (user_id,), fetchone=True))[
            0]
        return citchen1, citchen2, citchen3, citchen_status

    async def change_citchen(self, user_id: int, who: str, number):
        day = date.today().strftime("%Y-%m-%d")
        if who == 'conditer':
            await self.db_request('UPDATE res_staff SET chefs_status_1 = ? WHERE user_id = ?', (number[0], user_id))
            await self.db_request('UPDATE res_staff SET chefs_status_date = ? WHERE user_id = ?', (day, user_id))
        elif who == 'barmen':
            await self.db_request('UPDATE res_staff SET chefs_status_2 = ? WHERE user_id = ?', (number[1], user_id))
            await self.db_request('UPDATE res_staff SET chefs_status_date = ? WHERE user_id = ?', (day, user_id))
        elif who == 'chef':
            await self.db_request('UPDATE res_staff SET chefs_status_3 = ? WHERE user_id = ?', (number[2], user_id))
            await self.db_request('UPDATE res_staff SET chefs_status_date = ? WHERE user_id = ?', (day, user_id))
