# BOT MADE BY AvatarPid0r
import asyncio

from middleware import setup_middleware, setup_middleware_cheack_subs
from handlers import register_handlers
from config.bot_data import dp
from aiogram import executor
import logging

from utils.revenue_send_all import check_time_and_send

logging.basicConfig(level=logging.INFO)

    
async def on_startup(_):
    asyncio.create_task(check_time_and_send())
    setup_middleware(dp)
    setup_middleware_cheack_subs(dp)
    logging.info("-_-_- BOT MADE BY AvatarPid0r  -_-_-")

register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
