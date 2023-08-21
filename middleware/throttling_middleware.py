from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import Throttled
from config.bot_data import admin_id, dp
from aiogram import Dispatcher


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_call"
        if call.from_user.id not in admin_id:
            try:
                await dispatcher.throttle(key, rate=limit)
            except Throttled as t:
                await self.call_throttled(call, t)
                raise CancelHandler()

    async def on_process_message(self, message: Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        if message.from_user.id not in admin_id:
            try:
                await dispatcher.throttle(key, rate=limit)
            except Throttled as t:
                await self.message_throttled(message, t)
                raise CancelHandler()

    @staticmethod
    async def call_throttled(call: CallbackQuery, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await call.answer("❗ Пожалуйста, не спамьте ❗️", show_alert=True)

    @staticmethod
    async def message_throttled(message: Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await message.answer("❗ Пожалуйста, не спамьте ❗️")


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator

# dp.middleware.setup(ThrottlingMiddleware())
