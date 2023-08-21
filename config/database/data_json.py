import json
import codecs
import os


class Database_json:
    def __init__(self, db_path: str):
        self._db_path = db_path

    async def open(self):
        with codecs.open(self._db_path, 'r', 'utf-8') as file:
            value = eval(str(file.readline()))
        return value

    async def write(self, source):
        with codecs.open(str(self._db_path), 'w', 'utf-8') as file:
            value = file.write(str(source))
        return value

    async def create_partner(self, name: str) -> bool:
        db = await self.open()
        if 'partner' in db and name in db['partner']:
            return False
        else:
            db.setdefault('partner', {})
            db['partner'][name] = {}
            await self.write(db)
            return True

    async def del_partner(self, name: str) -> bool:
        db = await self.open()
        if 'partner' in db and name in db['partner']:
            del db['partner'][name]
            await self.write(db)
            return True
        else:
            return False

    async def add_certificat(self, path_: str, name_partner: str) -> []:
        db = await self.open()
        count = 0
        count_bad = 0
        good = []
        error = []
        with open(path_, 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    line = line.strip()
                    if line:
                        name, price, link, promo_code = [value.strip() for value in line.split(',')]
                        if name in db['partner'][name_partner]:
                            continue
                        db['partner'][name_partner][name] = {
                            'price': int(price),
                            'url': link,
                            'promocode': promo_code
                        }
                        await self.write(db)
                        count += 1

                except Exception as e:
                    count_bad += 1
            error.append(count_bad)
            good.append(count)
        os.remove(path_)
        return good, error

    async def del_cert(self, name: str, name_partner: str) -> bool:
        db = await self.open()
        if 'partner' in db and name in db['partner'][name_partner]:
            del db['partner'][name_partner][name]
            await self.write(db)
            return True
        else:
            return False

    async def cheack_partner(self, name: str) -> bool:
        db = await self.open()
        if 'partner' in db and name in db['partner']:
            return True
        else:
            return False

    async def cheack_all_partner(self) -> []:
        db = await self.open()
        m = db['partner']
        all = []
        for i in m.keys():
            all.append(i)

        return all

    async def cheack_all_cert(self, name: str) -> []:
        db = await self.open()
        m = db['partner'][name]
        all = []
        price = []
        for i in m.keys():
            all.append(i)
        for item in all:
            prices = db['partner'][name][item]['price']
            price.append(prices)


        return all, price

    async def cheack_price(self, partner: str, name: str) -> int:
        db = await self.open()
        price = db['partner'][partner][name]['price']
        return price

    async def del_certif_but(self, partner: str, name: str):
        db = await self.open()

        cheack = db['partner'][partner][name]
        url = cheack.get('url')
        promocode = cheack.get('promocode')

        del db['partner'][partner][name]
        await self.write(db)

        return url, promocode
