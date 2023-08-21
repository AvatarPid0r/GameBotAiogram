from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config.bot_data import admin_id, feedback_link, db, profile3, profile2, profile1
from config.bot_text import Text

cb = CallbackData("fabnum", "action")


def welcome_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🖥 Начать игру", callback_data=cb.new(action="start")))
    if user_id in admin_id:
        keyboard.add(InlineKeyboardButton("👤 Admin Menu", callback_data=cb.new(action="admin_menu")))
    return keyboard


def main_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🏪 Мой ресторан", callback_data=cb.new(action="profile")))
    keyboard.row(
        InlineKeyboardButton("👤 Персонал", callback_data=cb.new(action="personal")),
        InlineKeyboardButton("📦 Продукты", callback_data=cb.new(action="product")))
    keyboard.row(
        InlineKeyboardButton("💠 Обмен на сертификаты", callback_data="withdraw"),
        InlineKeyboardButton(text='💳 Вывести на карту', callback_data='show_calc'))
    keyboard.add(InlineKeyboardButton("💸 Заработать", callback_data=cb.new(action="start_earn")))
    keyboard.row(
        InlineKeyboardButton("📝 Информация о проекте", callback_data=cb.new(action="info")),
        InlineKeyboardButton("📌Топ", callback_data='show_top')
    )
    keyboard.add(
        InlineKeyboardButton("🎟 Активировать промокод", callback_data=cb.new(action="enter_promocode"))
    )
    if feedback_link:
        keyboard.add(InlineKeyboardButton("👉 Наши отзывы ⭐️", url=feedback_link))
    if user_id in admin_id:
        keyboard.add(InlineKeyboardButton("👤 Admin Menu", callback_data=cb.new(action="admin_menu")))
    return keyboard


show_top = InlineKeyboardMarkup(row_width=1)
m1 = InlineKeyboardButton(text='🌟Топ дня', callback_data='top_day')
m2 = InlineKeyboardButton(text='🏵Топ недели', callback_data='top_week')
m3 = InlineKeyboardButton(text='💠Топ месяца', callback_data='top_month')
m4 = InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu")
show_top.row(m1, m2).add(m3).add(m4)

show_vivod = InlineKeyboardMarkup()
m1 = InlineKeyboardButton(text="💳 Вывести на карту", switch_inline_query_current_chat='VAL_RUB=1000')
m4 = InlineKeyboardButton(text="🔙 Назад", callback_data=f"back|main_menu")
show_vivod.add(m1).add(m4)


def back_button(value: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔙 Назад", callback_data=f"back|{value}")
    )
    return keyboard


my_res = InlineKeyboardMarkup()
m3 = InlineKeyboardButton('Отзывы📋', callback_data='otziv')
m4 = InlineKeyboardButton('Книга жалоб📕', callback_data='jalob')
m1 = InlineKeyboardButton('⚙ Настройки витрины', callback_data='settings_vitrina')
m2 = InlineKeyboardButton('🆙 Улучшения', callback_data='improvement_')
m5 = InlineKeyboardButton('👨‍🍳 Управление кухней', callback_data='settings_citchen')
my_res.add(m3, m4).add(m1, m2).add(m5).add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))

earn_keyboard = InlineKeyboardMarkup(row_width=1)
earn_keyboard.add(
    InlineKeyboardButton("💥 Чаевые", callback_data=cb.new(action="clicker")),
    InlineKeyboardButton("💰 Задания", callback_data=cb.new(action="tasks")),
    InlineKeyboardButton("👥 Пригласить друзей", callback_data=cb.new(action="invite_friends")),
    InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu")
)

product_keyboard = InlineKeyboardMarkup(row_width=1)
product_keyboard.add(
    InlineKeyboardButton("Закуски", callback_data="buy_zakus_1"),
    InlineKeyboardButton("Напитки", callback_data="buy_drinks_2"),
    InlineKeyboardButton("Снэки", callback_data="buy_snacks_3"),
    InlineKeyboardButton("Десерты", callback_data="buy_desert_4"),
    InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu")
)

info_keyboard = InlineKeyboardMarkup(row_width=1)
m1 = InlineKeyboardButton(text='профиль1', url=profile1)
m2 = InlineKeyboardButton(text='профиль2', url=profile2)
m3 = InlineKeyboardButton(text='профиль3', url=profile3)
info_keyboard.row(m1, m2).row(m3).add(
    InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu")
)

personal_keyboard = InlineKeyboardMarkup(row_width=1)
personal_keyboard.add(
    InlineKeyboardButton("Официанты", callback_data="wait_oficiant"),
    InlineKeyboardButton("Склад", callback_data="wait_sklad"),
    InlineKeyboardButton("Кухня", callback_data="wait_kitchen"),
    InlineKeyboardButton("Маркетинг", callback_data="wait_pr"),
    InlineKeyboardButton("Административный отдел", callback_data="wait_administrator"),
    InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu")
)

clicker_menu = InlineKeyboardMarkup(row_width=1)
clicker_menu.add(
    InlineKeyboardButton("💥 Собрать чаевые", callback_data=cb.new(action="click")),
    InlineKeyboardButton("🔙 Назад", callback_data="back|earn_menu")
)


def complete_task_menu(value: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✅ Проверить", callback_data=f"check|{value}"),
        InlineKeyboardButton("🔙 Назад", callback_data="back|earn_menu")
    )
    return keyboard


admin_menu = InlineKeyboardMarkup(row_width=2)
admin_menu.add(InlineKeyboardButton("🖋 Создать рассылку", callback_data=cb.new(action="mailing_menu"))).row()
admin_menu.add(
    InlineKeyboardButton("➕ Добавить задание", callback_data=cb.new(action="add_task")),
    InlineKeyboardButton("➖ Удалить задание", callback_data=cb.new(action="delete_task")),
    InlineKeyboardButton("🎟 Создать промокод", callback_data=cb.new(action="create_promo")),
    InlineKeyboardButton("➖ Удалить промокод", callback_data=cb.new(action="delete_promo")),
    InlineKeyboardButton("📃 Статистика", callback_data=cb.new(action="statistic"))
).add(
    InlineKeyboardButton("➕ Добавить партнера", callback_data='create_partner'),
    InlineKeyboardButton("➖ Удалить партнера", callback_data='delete_partner'),
    InlineKeyboardButton("➕ Добавить сертификат", callback_data='add_cert'),
    InlineKeyboardButton("➖ Удалить сертификат", callback_data='del_cert'),
).add(InlineKeyboardButton(text='Создать событие', callback_data='create_event'))
admin_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu"))

add_task_menu = InlineKeyboardMarkup(row_width=2)
add_task_menu.add(
    InlineKeyboardButton("📃 Описание", callback_data=cb.new(action="change_description")),
    InlineKeyboardButton("💵 Вознаграждение", callback_data=cb.new(action="change_reward")),
    InlineKeyboardButton("🆔 Канала", callback_data=cb.new(action="change_channel_id"))
).row()
add_task_menu.add(InlineKeyboardButton("📤 Опубликовать задание", callback_data=cb.new(action="publish_task"))).row()
add_task_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu"))

confirm_menu = InlineKeyboardMarkup(row_width=1)
confirm_menu.add(
    InlineKeyboardButton("✅ Подтвердить", callback_data=cb.new(action="confirm")),
    InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu")
)

promo_menu = InlineKeyboardMarkup(row_width=2)
promo_menu.add(
    InlineKeyboardButton("🎟 Промокод", callback_data=cb.new(action="enter_promo")),
    InlineKeyboardButton("💵 Вознаграждение", callback_data=cb.new(action="enter_reward")),
    InlineKeyboardButton("📤 Опубликовать промокод", callback_data=cb.new(action="publish_promo"))
).row()
promo_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu"))

oficiant = InlineKeyboardMarkup(row_width=1)
oficiant.add(
    InlineKeyboardButton("Новичок", callback_data="ofic_1"),
    InlineKeyboardButton("Любитель", callback_data="ofic_2"),
    InlineKeyboardButton("Профессионал", callback_data="ofic_3"),
    InlineKeyboardButton("🔙Назад", callback_data=cb.new(action='personal'))
)

citchen = InlineKeyboardMarkup(row_width=1)
citchen.add(
    InlineKeyboardButton("Кондитер", callback_data="citchen_1"),
    InlineKeyboardButton("Бармен", callback_data="citchen_2"),
    InlineKeyboardButton("Шеф-повар", callback_data="citchen_3"),
    InlineKeyboardButton("🔙Назад", callback_data=cb.new(action='personal'))
)

marketing = InlineKeyboardMarkup(row_width=1)
marketing.add(
    InlineKeyboardButton("Промоутеры", callback_data="marketpromo_1"),
    InlineKeyboardButton("Маркетологи", callback_data="marketmarketing_2"),
    InlineKeyboardButton("PR-отдел", callback_data="marketpr_3"),
    InlineKeyboardButton("🔙Назад", callback_data=cb.new(action='personal'))
)

administration = InlineKeyboardMarkup(row_width=1)
administration.add(
    InlineKeyboardButton("Новичок", callback_data="admin_1"),
    InlineKeyboardButton("Любитель", callback_data="admin_2"),
    InlineKeyboardButton("Профессионал", callback_data="admin_3"),
    InlineKeyboardButton("🔙Назад", callback_data=cb.new(action='personal'))
)

sklad = InlineKeyboardMarkup(row_width=1)
sklad.add(
    InlineKeyboardButton('Маленький', callback_data='sklad_1'),
    InlineKeyboardButton('Средний', callback_data='sklad_2'),
    InlineKeyboardButton('Большой', callback_data='sklad_3'),
    InlineKeyboardButton("🔙Назад", callback_data=cb.new(action='personal'))
)


async def buyofic(tip: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton('Да', callback_data=f'buyofic_{tip}')
    m2 = InlineKeyboardButton('🔙Назад', callback_data=f'wait_oficiant')
    markup.add(m1).add(m2)
    return markup


backofic = InlineKeyboardMarkup(row_width=1)
backofic.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'wait_oficiant')
)


async def buysklad(tip: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton('Да', callback_data=f'buysklad_{tip}')
    m2 = InlineKeyboardButton('🔙Назад', callback_data=f'wait_sklad')
    markup.add(m1).add(m2)
    return markup


backsklad = InlineKeyboardMarkup(row_width=1)
backsklad.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'wait_sklad')
)


async def buycitchen(tip: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton('Да', callback_data=f'buycitchen_{tip}')
    m2 = InlineKeyboardButton('🔙Назад', callback_data=f'wait_kitchen')
    markup.add(m1).add(m2)
    return markup


backcitchen = InlineKeyboardMarkup(row_width=1)
backcitchen.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'wait_kitchen')
)


async def buymarketol(tip: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton('Да', callback_data=f'buymarketolog_{tip}')
    m2 = InlineKeyboardButton('🔙Назад', callback_data=f'wait_pr')
    markup.add(m1).add(m2)
    return markup


backmarketol = InlineKeyboardMarkup(row_width=1)
backmarketol.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'wait_pr')
)


async def buyadmins(tip: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    m1 = InlineKeyboardButton('Да', callback_data=f'buyadminist_{tip}')
    m2 = InlineKeyboardButton('🔙Назад', callback_data=f'wait_administrator')
    markup.add(m1).add(m2)
    return markup


backadmins = InlineKeyboardMarkup(row_width=1)
backadmins.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'wait_administrator')
)

backproduct = InlineKeyboardMarkup(row_width=1)
backproduct.add(
    InlineKeyboardButton('🔙Назад', callback_data=f'back|product')
)


async def confirm_product(product: int, count: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton(text='Да', callback_data=f'confirm_{product}_{count}')
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='back|product')
    keyboard.row(confirm_button).row(back_button)
    return keyboard


async def improvement_markup(user_id: int) -> InlineKeyboardMarkup:
    improvement_1, improvement_2, improvement_3, improvement_4, improvement_5 = await db.cheack_improvement(
        user_id=user_id)
    improvement_markup = InlineKeyboardMarkup(row_width=1)
    improvement_markup.add(
        InlineKeyboardButton(text=Text.improvement1.format(wai=improvement_1), callback_data='improvement_1'),
        InlineKeyboardButton(text=Text.improvement2.format(wai=improvement_2), callback_data='improvement_2'),
        InlineKeyboardButton(text=Text.improvement3.format(wai=improvement_3), callback_data='improvement_3'),
        InlineKeyboardButton(text=Text.improvement4.format(wai=improvement_4), callback_data='improvement_4'),
        InlineKeyboardButton(text=Text.improvement5.format(wai=improvement_5), callback_data='improvement_5'),
        InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action='profile'))
    )
    return improvement_markup


async def confirm_improvement(product: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton(text='Да', callback_data=f'improvementconfirm_{product}')
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='improvement_')
    keyboard.row(confirm_button).row(back_button)
    return keyboard


events = InlineKeyboardMarkup()
m1 = InlineKeyboardButton(text='👨 Клиентов в сутки', callback_data='up_client')
m2 = InlineKeyboardButton(text='💳 Баланс', callback_data='event_balance')
m3 = InlineKeyboardButton(text='🍀 Шанс', callback_data='fart_event')
m4 = InlineKeyboardButton(text='✅ Повезет', callback_data='event_yes')
m5 = InlineKeyboardButton(text='❌ Не повезет', callback_data='event_no')
m7 = InlineKeyboardButton(text='📌 Отправить событие', callback_data='event_send')
m6 = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="admin_menu"))
events.add(m1, m2).add(m3).add(m4, m5).add(m7).add(m6)

backevent = InlineKeyboardMarkup()
m1 = InlineKeyboardButton(text='🔙Назад', callback_data='create_event')
backevent.add(m1)

confirm_event = InlineKeyboardMarkup()
m1 = InlineKeyboardButton(text='Да', callback_data='send_event_all')
m2 = InlineKeyboardButton(text='🔙Назад', callback_data='create_event')
confirm_event.add(m1).add(m2)

confirm_citchen = InlineKeyboardMarkup()
m1 = InlineKeyboardButton(text='Да', callback_data='confirmcitchen')
m2 = InlineKeyboardButton(text='🔙Назад', callback_data='settings_citchen')
confirm_citchen.add(m1).add(m2)


async def get_status(citc1: int, citc2: int, citc3: int) -> InlineKeyboardMarkup:
    settings_citc = InlineKeyboardMarkup()
    work = '✅'
    no_work = '❌'
    m1 = InlineKeyboardButton(text='Кондитер ➡', callback_data='None')
    m2 = InlineKeyboardButton(text=f'Работает {work if citc1 == 0 else no_work}', callback_data='change_conditer')
    m3 = InlineKeyboardButton(text='Бармер ➡', callback_data='None')
    m4 = InlineKeyboardButton(text=f'Работает {work if citc2 == 0 else no_work}', callback_data='change_barmen')
    m5 = InlineKeyboardButton(text='Шеф-повар ➡', callback_data='None')
    m6 = InlineKeyboardButton(text=f'Работает {work if citc3 == 0 else no_work}', callback_data='change_chef')
    back = InlineKeyboardButton(text='🔙Назад', callback_data=cb.new(action="profile"))
    settings_citc.add(m1, m2).add(m3, m4).add(m5, m6).add(back)
    return settings_citc