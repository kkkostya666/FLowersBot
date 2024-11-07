import datetime
from functools import partial

from aiogram.types import InputFile, FSInputFile

from keyboards.select_city_keyboard import set_sity
from keyboards.autorizate.autorizate_keyboard import autorizate_keyboard, only_register, only_autorizate, \
    reply_keyboard
from aiogram import types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from text.start.start import start_message
from aiogram import Router


class StartHandler:
    def __init__(self, db, chat_id, bot_token):
        self.bot = Bot(token=bot_token)
        self.router = Router()
        self.db = db
        self.register_handlers()
        self.chat_id = chat_id

    def register_handlers(self):
        self.router.message(CommandStart())(self.start)
        cities = {"moskow": "Москва", "piter": "Санкт-Петербург", "kzn": "Казань", "samara": "Самара", "yfa": "Уфа",
                  "perm": "Пермь", "volgograd": "Волгоград", "novosib": "Новосибирск", "nizhiy": "Нижний Новгород",
                  "izhevsk": "Ижевск", "tolyati": "Тольятти", "habarovks": "Хабаровск", "tymen": "Тюмень",
                  "chelny": "Набережные Челны"}
        self.router.callback_query(F.data == 'register')(self.register)
        for callback_data, city_name in cities.items():
            self.router.callback_query(F.data == callback_data)(partial(self.process_city, city_name))

    async def start(self, message: types.Message, state: FSMContext):
        await state.clear()
        if self.db.user_exists(message.from_user.id):
            await message.answer(text=start_message,
                                 parse_mode="HTML",
                                 reply_markup=await reply_keyboard())
        else:
            await message.answer("<i>❗ Вам необходимо зарегистрироваться</i>",
                                 reply_markup=await only_register(),
                                 parse_mode="HTML")

    async def register(self, callback_query: types.CallbackQuery):
        if not self.db.user_exists(callback_query.from_user.id):
            await callback_query.message.answer("<b>Выберите город 🌇</b>",
                                                parse_mode="HTML",
                                                reply_markup=await set_sity())
        else:
            await callback_query.message.answer("<b>✖️ ВАШ АККАУНТ ЗАРЕГИСТРИРОВАН</b>\n\n‼️ Авторизируйтесь",
                                                parse_mode="HTML",
                                                reply_markup=await only_autorizate())
        await callback_query.message.delete()

    async def process_city(self, city, callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        self.db.add_user(callback_query.from_user, city, datetime.datetime.now())
        text = (f"<b>💰 Зарегистрирован новый пользователь</b>\n\n"
                f"____\n"
                f"USERNAME - @{callback_query.from_user.username}\n"
                f"ID - <code>{callback_query.from_user.id}</code>\n"
                f"Имя - <code>{callback_query.from_user.first_name}</code>\n"
                f"Фамилия - <code>{callback_query.from_user.last_name}</code>\n"
                f"Язык пользователя - <code>{callback_query.from_user.language_code}</code>\n"
                f"Город - <code>{city}</code>\n"
                f"____")

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode="HTML",
        )

        await callback_query.message.answer(text=start_message,
                                            parse_mode="HTML",
                                            reply_markup=await reply_keyboard())
