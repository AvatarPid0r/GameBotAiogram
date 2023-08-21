from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import UserDeactivated
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.bot_data import db, balance_for_referral, money_name
from config.bot_text import Text
import markups as nav

class GroupMembershipMiddleware(BaseMiddleware):
    def __init__(self, group_id, channel_link):
        super().__init__()
        self.group_id = group_id
        self.channel_link = channel_link

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = message.from_user
        if user.is_bot:
            return
        is_member = await self.check_membership(user.id)
        try:
            referall_id = message.text[7:]
            if referall_id != '' and referall_id.isdigit():
                try:
                    if not await db.client_exists(message.from_user.id, table="referral"):
                        await db.add_referral(user_id=message.from_user.id, referrer_id=referall_id)
                        referrer_balance = await db.get_client_date(referall_id, ("balance",))
                        new_balance = referrer_balance[0] + balance_for_referral
                        await db.update_data(referall_id, ("balance", new_balance,))
                        await self.bot.send_message(referall_id,
                                               f"🎉 У вас новый реферал(<code>@{message.from_user.username if message.from_user.username is not None else 'Noname'}</code>), "
                                               f"ваш баланс пополнен на <code>{balance_for_referral}</code> {money_name}\n\n На вашем балансе <code>{new_balance}</code> {money_name}",
                                               reply_markup=nav.back_button("main_menu"))
                except Exception as e:
                    pass
        except:
            pass


        if not is_member:
            markup = InlineKeyboardMarkup()
            m1 = InlineKeyboardButton(text='Подписка📌', url=self.channel_link)
            m2 = InlineKeyboardButton(text='✅ Подписался', callback_data='start')
            markup.add(m2).add(m1)
            try:
                await self.bot.delete_message(chat_id=user.id, message_id=message.message_id)
                await message.answer(text=Text.dont_subscribe, reply_markup=markup)
            except:
                pass
            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        user = query.from_user
        if user.is_bot:
            return
        is_member = await self.check_membership(user.id)
        if not is_member:
            markup = InlineKeyboardMarkup()
            m1 = InlineKeyboardButton(text='Подписка📌', url=self.channel_link)
            m2 = InlineKeyboardButton(text='✅ Подписался', callback_data='start')
            markup.add(m2).add(m1)
            try:
                await self.bot.delete_message(chat_id=user.id, message_id=query.message.message_id)
                await self.bot.send_message(chat_id=user.id, text=Text.dont_subscribe, reply_markup=markup)
            except:
                pass
            raise CancelHandler()

    async def check_membership(self, user_id):
        try:
            chat_member = await self.bot.get_chat_member(chat_id=self.group_id, user_id=user_id)
            if chat_member.status in ["member", "creator", "administrator"]:
                return True
            else:
                return False
        except UserDeactivated:
            return False
