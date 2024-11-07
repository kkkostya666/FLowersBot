from datetime import datetime
import re

from aiogram import types, F, Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext

from keyboards.support_keyboard.support_keyboard import support_keyboard
from state import SupportState


class SupportHandler:
    def __init__(self, db, chat_id, bot_token):
        self.bot = Bot(token=bot_token)
        self.db = db
        self.router = Router()
        self.register_handlers()
        self.chat_id = chat_id

    def register_handlers(self):
        self.router.callback_query(F.data == 'support')(self.support)
        self.router.callback_query(F.data == 'support_send')(self.support_send)
        self.router.message.register(self.support_text, lambda message: message.text == "🛠️ ТЕХНИЧЕСКАЯ ПОДДЕРЖКА")
        self.router.message(SupportState.TextModel.text)(self.send_message)
        self.router.message(SupportState.TextModel.text_support)(self.send_message_support)

    @staticmethod
    async def support(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(text=f"<b>Напишите Ваш вопрос или пожелание</b>", parse_mode="HTML")
        await state.set_state(SupportState.TextModel.text)

    @staticmethod
    async def support_text(message: types.Message, state: FSMContext):
        await message.answer(text=f"<b>Напишите Ваш вопрос или пожелание</b>", parse_mode="HTML")
        await state.set_state(SupportState.TextModel.text)

    async def send_message(self, message: types.Message, state: FSMContext):
        self.db.add_support_request(user_id=message.from_user.id, message=message.text)
        data = self.db.get_latest_support_request(user_id=message.from_user.id)
        text = (f"<b>👨 Новое обращение от пользователя @{message.from_user.username}</b>\n"
                f"<i>ID Заявки:</i> {data[0]}\n"
                f"<i>Статус:</i> {data[5]}\n"
                f"<i>Дата обращения:</i> {data[3]}\n"
                f"________\n\n"
                f"<i>{message.text}</i>\n\n"
                f"________\n\n"
                f"❗️ Для настройки стандартного сообщения нужно перейти в настройки")
        await self.bot.send_message(chat_id=self.chat_id,
                                    text=text,
                                    reply_markup=await support_keyboard(),
                                    parse_mode="HTML")
        await message.answer(
            text=(f"<i>ID Заявки:</i> {data[0]}\n\n"
                  f"________\n"
                  f"<i>Статус:</i> {data[5]}\n"
                  f"<i>Дата обращения:</i> {data[3]}\n"
                  f"________\n\n"
                  "<i>Ожидайте ответ от наших операторов</i>\n"
                  "<i>В среднем ожидание составляет 15 минут</i>"),
            parse_mode="HTML"
        )
        await message.delete()
        await state.clear()

    @staticmethod
    async def support_send(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(text=f"<b>Напишите ответ пользователю</b>", parse_mode="HTML")
        await state.set_state(SupportState.TextModel.text_support)
        await callback.message.delete()

    async def send_message_support(self, message: types.Message, state: FSMContext):
        data_id = self.db.get_latest_support_request(user_id=message.from_user.id)
        print(data_id[0])
        self.db.update_support_request_response(support_id=data_id[0],
                                                response=message.text,
                                                status="☑️ Ответ получен")
        data = self.db.get_latest_support_request(user_id=message.from_user.id)
        datatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = (f"<b>☑️ Пришел ответ от операторов поддержки</b>\n\n"
                f"<i>ID Заявки:</i> {data[0]}\n\n"
                f"<i>Статус:</i> {data[5]}\n"
                f"<i>Дата ответа:</i> {datatime}\n"
                f"________\n"
                f"<i>{data[4]}</i>\n"
                f"________\n\n"
                )
        await self.bot.send_message(chat_id=data[1],
                                    text=text,
                                    parse_mode="HTML")
        await message.answer(text="<b>Ваш ответ успешно отпрвлен</b>\n\n",
                             parse_mode="HTML")
        await message.delete()
        await state.clear()
