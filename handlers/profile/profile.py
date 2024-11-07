from functools import partial

from aiogram import types, F
from aiogram import Router
from aiogram.types import FSInputFile

from keyboards.profile.profile_keyboard import profile_keyboard
from keyboards.select_city_keyboard import set_sity_update
from keyboards.select_currency_keyboard import set_currency


class ProfileHandler:
    def __init__(self, db):
        self.router = Router()
        self.db = db
        self.register_handlers()

    def register_handlers(self):
        self.router.message.register(self.profile, lambda message: message.text == "👤 ПРОФИЛЬ")
        self.router.callback_query(F.data == 'change_city')(self.change_city)
        cities = {"moskow_update": "Москва", "piter_update": "Санкт-Петербург", "kzn_update": "Казань",
                  "samara_update": "Самара", "yfa_update": "Уфа",
                  "perm_update": "Пермь", "volgograd_update": "Волгоград", "novosib_update": "Новосибирск",
                  "nizhiy_update": "Нижний Новгород",
                  "izhevsk_update": "Ижевск", "tolyati_update": "Тольятти", "habarovks_update": "Хабаровск",
                  "tymen_update": "Тюмень",
                  "chelny_update": "Набережные Челны"}
        for callback_data, city_name in cities.items():
            self.router.callback_query(F.data == callback_data)(partial(self.update_city, city_name))
        self.router.callback_query(F.data == 'change_currency')(self.change_currency)
        self.router.callback_query(F.data == 'my_zakaz')(self.my_zakaz)
        currency = {"RUB": "🇷🇺 RUB", "sbp": "📱 SBP", "usdt": "💲 USDT",
                    "btc": "💶 BTC"}
        for callback_data, currency_name in currency.items():
            self.router.callback_query(F.data == callback_data)(partial(self.update_currency, currency_name))

    async def profile(self, message: types.Message):
        data = self.db.get_user_by_id(message.from_user.id)
        count_model = self.db.count_models_with_city(data[8])
        count_order = self.db.count_orders_by_user_id(data[0])
        print(count_order)
        current_currency = data[9] if data[9] is not None else "Неопределено"
        profile = (f"👨‍💻 <b>USERNAME:</b> {message.from_user.username}\n\n"
                   f"____\n\n"
                   f"<i>🪝 ID: {data[0]}</i>\n"
                   f"<i>⭐️ Рейтинг: 0</i>\n"
                   f"<i>⚡️ Количество заказов: {count_order}</i>\n"
                   f"<i>🏙 Текущий город: {data[8]}</i>\n"
                   f"<i>💰 Текущая валюта: {current_currency}</i>\n\n"
                   f"____\n\n"
                   f"❗️ <b>Количество доступных букетов в выбранном городе: {count_model}</b>")
        await message.answer(
            text=profile,
            parse_mode="HTML",
            reply_markup=await profile_keyboard())

    @staticmethod
    async def change_city(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer(
            text="Выберите город",
            parse_mode="HTML",
            reply_markup=await set_sity_update())
        await callback.answer()

    async def update_city(self, city, callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        self.db.update_user_city(callback_query.from_user.id, city)
        await callback_query.message.answer(f"☑️ <i>Ваш город был изменён на {city}</i>", parse_mode="HTML")
        data = self.db.get_user_by_id(callback_query.from_user.id)
        count_model = self.db.count_models_with_city(data[8])
        count_order = self.db.count_orders_by_user_id(data[0])
        print(data[8], count_model)
        current_currency = data[9] if data[9] is not None else "Неопределено"
        profile = (f"👨‍💻 <b>USERNAME:</b> {callback_query.from_user.username}\n\n"
                   f"____\n\n"
                   f"<i>🪝 ID: {data[0]}</i>\n"
                   f"<i>⭐️ Рейтинг: 0</i>\n"
                   f"<i>⚡️ Количество заказов: {count_order}</i>\n"
                   f"<i>🏙 Текущий город: {data[8]}</i>\n"
                   f"<i>💰 Текущая валюта: {current_currency}</i>\n\n"
                   f"____\n\n"
                   f"❗️ <b>Количество доступных букетов в выбранном городе: {count_model}</b>")
        await callback_query.message.answer(
            text=profile,
            parse_mode="HTML",
            reply_markup=await profile_keyboard())

    @staticmethod
    async def change_currency(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer(
            text="Выберите доступную валюту",
            parse_mode="HTML",
            reply_markup=await set_currency())
        await callback.answer()

    async def update_currency(self, currency, callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        self.db.update_user_currency(callback_query.from_user.id, currency)
        await callback_query.message.answer(f"☑️ <i>Ваша валюта была изменёна на {currency}</i>", parse_mode="HTML", )
        data = self.db.get_user_by_id(callback_query.from_user.id)
        count_model = self.db.count_models_with_city(data[8])
        count_order = self.db.count_orders_by_user_id(data[0])
        print(data[8], count_model)
        current_currency = data[9] if data[9] is not None else "Неопределено"
        profile = (f"👨‍💻 <b>USERNAME:</b> {callback_query.from_user.username}\n\n"
                   f"____\n\n"
                   f"<i>🪝 ID: {data[0]}</i>\n"
                   f"<i>⭐️ Рейтинг: 0</i>\n"
                   f"<i>⚡️ Количество заказов: {count_order}</i>\n"
                   f"<i>🏙 Текущий город: {data[8]}</i>\n"
                   f"<i>💰 Текущая валюта: {current_currency}</i>\n\n"
                   f"____\n\n"
                   f"❗️ <b>Количество доступных букетов в выбранном городе: {count_model}</b>")
        await callback_query.message.answer(
            text=profile,
            parse_mode="HTML",
            reply_markup=await profile_keyboard())

    async def my_zakaz(self, callback: types.CallbackQuery):
        await callback.message.delete()

        user_id = self.db.get_user_by_id(callback.from_user.id)[0]
        orders = self.db.get_orders_by_user_id(user_id)

        if not orders:
            await callback.message.answer("У вас нет активных заказов.")
            return

        order_texts = []
        for order in orders:
            order_texts.append(
                f"🧾 <b>ЗАКАЗ #{order[1]}</b>\n"
                f"<i>Метод оплаты:</i> <code>{order[7] if order[7] else 'Не указано'}</code>\n"
                f"<i>Сумма к оплате:</i> <code>{order[4]}</code>\n"
                f"<i>Статус:</i> <code>{order[5]}</code>\n"
                f"<i>Время:</i> <code>{order[7]}</code>\n"
                f"-------\n"
            )
        await callback.message.answer(
            text="\n".join(order_texts),
            reply_markup=await profile_keyboard(),
            parse_mode="HTML",
        )
