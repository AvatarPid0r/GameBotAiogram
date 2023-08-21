from aiogram import Dispatcher
from middleware.throttling_middleware import ThrottlingMiddleware
from middleware.check_subscribe import GroupMembershipMiddleware
from config.bot_data import channel, bot, channel_link


def setup_middleware(dp: Dispatcher):
    # dp.middleware.setup(ThrottlingMiddleware())
    pass

def setup_middleware_cheack_subs(dp: Dispatcher):
    middleware = GroupMembershipMiddleware(group_id=channel, channel_link=channel_link)
    middleware.bot = bot
    dp.middleware.setup(middleware)
