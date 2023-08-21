from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from itertools import islice
from config.bot_text import Text as text
from config.bot_data import db_json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Paginator:
    def __init__(self,
                 data: types.InlineKeyboardMarkup,
                 callback_startswith: str = 'page|',
                 size: int = 8,
                 page_separator: str = '/',
                 dp: Dispatcher = None,
                 back_callback: str = "main_menu"):
        self.dp = dp
        self._page_separator = page_separator
        self._startswith = callback_startswith
        self._size = size
        self._back_callback = f"back|{back_callback}"
        if isinstance(data, (types.InlineKeyboardMarkup, types.InlineKeyboardButton)):
            self._keyboard_list = list(
                self._chunk(
                    it=data.inline_keyboard,
                    size=self._size
                )
            )
        else:
            raise ValueError(f"{data} is not valid data")

    @staticmethod
    def _chunk(it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    @staticmethod
    def _get_page(call: types.CallbackQuery) -> int:
        return int(call.data[call.data.find("|") + 1:])

    def _get_paginator(self,
                       counts: int,
                       page: int,
                       page_separator: str = '/',
                       startswith: str = 'page|'
                       ) -> list:
        counts -= 1
        paginations = []
        if page > 0:
            paginations.append(
                types.InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}{page - 1}'
                ),
            )
        paginations.append(
            types.InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                types.InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}{page + 1}'
                )
            )
        return paginations

    def __call__(
            self,
            current_page=0,
            *args,
            **kwargs
    ) -> types.InlineKeyboardMarkup:
        _list_current_page = self._keyboard_list[current_page]
        paginations = self._get_paginator(
            counts=len(self._keyboard_list),
            page=current_page,
            page_separator=self._page_separator,
            startswith=self._startswith
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[*_list_current_page, paginations]).add(
            types.InlineKeyboardButton(text="🔙 Назад", callback_data=self._back_callback))
        if self.dp:
            self.paginator_handler()
        return keyboard

    def paginator_handler(self) -> tuple:
        async def _page(call: types.CallbackQuery):
            page = self._get_page(call)
            await call.message.edit_reply_markup(
                reply_markup=self.__call__(
                    current_page=page
                )
            )

        if not self.dp:
            return _page, Text(startswith=self._startswith)
        else:
            self.dp.register_callback_query_handler(
                _page,
                Text(startswith=self._startswith),
            )





class PaginationPartner:
    def __init__(self, items_per_page, names):
        self.items_per_page = items_per_page
        self.names = names

    def get_page_count(self):
        return len(self.names) // self.items_per_page + (1 if len(self.names) % self.items_per_page > 0 else 0)

    def get_page_buttons(self, page):
        start_index = (page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        names_on_page = self.names[start_index:end_index]

        buttons = []
        for name in names_on_page:
            button = InlineKeyboardButton(name, callback_data=f'partner_{name}')
            buttons.append(button)

        return buttons

    def get_pagination_markup(self, page):
        markup = InlineKeyboardMarkup(row_width=1)

        buttons = self.get_page_buttons(page)
        markup.add(*buttons)

        page_count = self.get_page_count()
        prev_page_button = InlineKeyboardButton('⬅️', callback_data='prev_page')
        next_page_button = InlineKeyboardButton('➡️', callback_data='next_page')
        current_page_button = InlineKeyboardButton(f'{page}/{page_count}', callback_data='current_page')

        if page == 1:
            prev_page_button = InlineKeyboardButton('⬅️', callback_data='none')
        if page == page_count:
            next_page_button = InlineKeyboardButton('➡️', callback_data='none')

        markup.row(prev_page_button, current_page_button, next_page_button)

        return markup



class PaginationCert:
    def __init__(self, items_per_page, names, partner, price):
        self.items_per_page = items_per_page
        self.names = names
        self.partner = partner
        self.price = price

    def get_page_count(self):
        return len(self.names) // self.items_per_page + (1 if len(self.names) % self.items_per_page > 0 else 0)

    def get_page_buttons(self, page):
        start_index = (page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        names_on_page = self.names[start_index:end_index]

        buttons = []
        for name, price in zip(names_on_page, self.price):
            button = InlineKeyboardButton(f'{name} [{price}]', callback_data=f'buycert_{self.partner}_{name}')
            buttons.append(button)

        return buttons


    def get_pagination_markup(self, page):
        markup = InlineKeyboardMarkup(row_width=1)

        buttons = self.get_page_buttons(page)
        markup.add(*buttons)

        page_count = self.get_page_count()
        prev_page_button = InlineKeyboardButton('⬅️', callback_data='prepagecert')
        next_page_button = InlineKeyboardButton('➡️', callback_data='nextpagecert')
        current_page_button = InlineKeyboardButton(f'{page}/{page_count}', callback_data='current_page')

        if page == 1:
            prev_page_button = InlineKeyboardButton('⬅️', callback_data='none')
        if page == page_count:
            next_page_button = InlineKeyboardButton('➡️', callback_data='none')

        markup.row(prev_page_button, current_page_button, next_page_button)

        return markup








