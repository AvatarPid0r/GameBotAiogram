from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    class AddTask(StatesGroup):
        data = State()
        description = State()
        reward = State()
        task_id = State()

    class DeleteTask(StatesGroup):
        task_id = State()

    class Mailing(StatesGroup):
        get_data = State()
        get_confirm = State()

    class AddPromo(StatesGroup):
        data = State()
        get_promo = State()
        get_reward = State()

    class DeletePromo(StatesGroup):
        get_promo = State()

    class AddPartner(StatesGroup):
        name = State()
        del_name = State()
        add_cert = State()
        add_cert1 = State()
        del_cert = State()
        del_cert1 = State()

    class CreateEvent(StatesGroup):
        text = State()


class Client(StatesGroup):
    class Promo(StatesGroup):
        get_promo = State()

    class Create_res(StatesGroup):
        name = State()

    class Card(StatesGroup):
        recv = State()


class Product(StatesGroup):
    text = State()
