from aiogram import types, F
from aiogram import Router
from aiogram.types import FSInputFile

from keyboards.main.main_keyboards import menu_keyboard


class MenuHandler:
    def __init__(self, db):
        self.router = Router()
        self.db = db
        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.profile, lambda message: message.text == "♻️ ГЛАВНОЕ МЕНЮ")

    async def profile(self, message: types.Message):
        await message.answer(
            text="📍 Главное меню\n\n<i>ниже представлены доступные категории наших красивых букетов❤️</i>",
            reply_markup=await menu_keyboard(),
            parse_mode="HTML",
        )



