from handlers.client import start, main_menu, back_button, complete_tasks, withdraw, use_promo, dp
from handlers.admin import adm_main_menu, statistic, tasks, mailing, promo, dp
from aiogram import Dispatcher

def register_handlers(dp: Dispatcher):
    start.register_handler_client_start(dp)
    main_menu.register_handler_client_main(dp)
    back_button.register_handler_client_back(dp)
    complete_tasks.register_handler_client_tasks(dp)
    adm_main_menu.register_handler_admin_main(dp)
    statistic.register_handler_admin_statistic(dp)
    tasks.register_handler_admin_tasks(dp)
    mailing.register_handler_admin_mailing(dp)
    promo.register_handler_admin_promo(dp)
    use_promo.register_handler_client_promo(dp)
