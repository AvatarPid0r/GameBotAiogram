from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from config.database.data import DataBase
from config.database.data_json import Database_json
import os

db = DataBase(os.path.join(os.getcwd(), "config", "database", "data.db"))
db_json = Database_json(os.path.join(os.getcwd(), "config", 'database', 'partners.json'))

# _________________________Настройка Бота____________________________
admin_id = []
token = ""
# ___________________________________________________________________
channel = -
channel_for_log = -
channel_link = ''
# ___________________________________________________________________
balance_for_referral = 20
balance_for_click1: int = 500  # Размер чаявых от
balance_for_click2: int = 5000 # Размер чаявых до
money_name = "рестиков" # Название моент
bot_username = "" # имя бота
min_withdraw = 200
redirect_link = "https://ya.ru"
min_referrer_withdraw = 1
feedback_link = "" # Если есть ссылка то появится отдельная кнопка с ссылкой на канал отзывов
procent_to_referal: float = 0.1  # добавляет баланс тому кто привел реферала, указывается в процентах (0.05 = 5%, 0.1 = 10% и так далее)
items_per_page = 10  # кол-во отоброжение партнеров
items_per_page1 = 10  # кол-во отоброжение сертификатов

profile1 = 'https://ya.ru'
profile2 = 'https://ya.ru' # профиль к кнопке о информацие о проекте
profile3 = 'https://ya.ru'
# ___________________________________________________________________
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
