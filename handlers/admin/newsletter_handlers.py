import os
import re
from functools import wraps

from aiogram import types, F, Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext

from state.NewSlatterState import NewSlatter


class NewSletterHandler:
    def __init__(self, db, chat_id, bot_token):
        self.router = Router()
        self.db = db
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.newsletter, lambda message: message.text == "🔎 РАССЫЛКА")
        self.router.message(NewSlatter.text)(self.add_newsletter)

    @staticmethod
    def chat_id_required(func):
        @wraps(func)
        async def wrapper(self, obj, *args, **kwargs):
            if isinstance(obj, types.Message):
                chat_id = obj.chat.id
            elif isinstance(obj, types.CallbackQuery):
                chat_id = obj.message.chat.id
            else:
                return
            if chat_id != self.chat_id:
                return

            return await func(self, obj, *args, **kwargs)

        return wrapper

    @chat_id_required
    async def newsletter(self, message: types.Message, state: FSMContext):
        await message.answer("Напиши текст для рассылки")
        await state.set_state(NewSlatter.text)

    @chat_id_required
    async def add_newsletter(self, message: types.Message, state: FSMContext):
        await message.delete()
        get_all = self.db.get_all_users()
        for subscriber in get_all:
            try:
                await self.bot.send_message(subscriber[1], message.text)
                await message.answer(text="Расслышка успешно запущена")
                await state.clear()
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {subscriber[0]}: {e}")
