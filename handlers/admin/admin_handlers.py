import os
import re
from functools import wraps, partial

from aiogram import types, F, Bot
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import config.token
from keyboards.admin_keyboard.admin_keyboard import admin_keyboard, admin_models_keyboard, \
    admin_models_category_keyboard, admin_models_keyboard_add, requisite_keyboard
from keyboards.admin_keyboard.order_keyboard import add_number_users
from keyboards.main.main_keyboards import menu_keyboard
from keyboards.select_currency_keyboard import set_currency_admin
from state.AddCategory import AddCategory
from state.AddModel import AddModel
from state.AppRequisiteAdmin import AddRequisite


class AdminHandler:
    def __init__(self, db, chat_id, bot_token):
        self.router = Router()
        self.db = db
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
        self.register_handlers()

    def register_handlers(self):
        self.router.message(Command("admin"))(self.admin)
        self.router.message.register(self.models, lambda message: message.text == "👧 Управление букетами")
        self.router.message.register(self.requisite, lambda message: message.text == "🛠️ Управление реквизитами")
        self.router.callback_query(F.data == 'category_model')(self.сategory_models)
        self.router.callback_query(F.data == 'good')(self.good)
        self.router.callback_query(F.data == 'cancel_order')(self.cancel_order)
        self.router.callback_query(F.data == 'add_requisite')(self.add_requisite)
        self.router.callback_query(F.data == 'model')(self.model)
        self.router.callback_query(F.data == 'add_category')(self.add_category)
        self.router.callback_query(F.data == 'delete_category')(self.delete_category)
        self.router.callback_query(F.data == 'add_model')(self.add_model)
        self.router.callback_query(F.data == 'add_number_phone')(self.add_number_phone)
        self.router.message(AddCategory.name)(self.add_category_db)
        self.router.message(AddCategory.delete_name)(self.delete_category_name)
        self.router.message(AddModel.name_model)(self.add_name_model)
        self.router.message(AddModel.description)(self.add_description_model)
        self.router.message(AddModel.weight)(
            self.add_price_full_night_model)  # Mapping 'weight' state to final price input
        self.router.message(AddModel.image)(self.add_image_model)
        self.router.callback_query(F.data.startswith('category_'))(self.category_selected)
        self.router.callback_query(F.data.startswith('city_'))(self.city_selected)
        currency = {"RUB_admin": "🇷🇺 RUB", "sbp_admin": "📱 SBP", "usdt_admin": "💲 USDT", "btc_admin": "💶 BTC"}
        for callback_data, currency_name in currency.items():
            self.router.callback_query(F.data == callback_data)(partial(self.update_requisite, currency_name))
        self.router.message(AddRequisite.number_card)(self.add_requisite_db)

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

    @staticmethod
    def is_number_required(func):
        @wraps(func)
        async def wrapper(message: types.Message):
            try:
                float(message.text)
                return await func(message, )
            except ValueError:
                await message.answer("Пожалуйста, введите корректное число.")
                return

        return wrapper

    @chat_id_required
    async def admin(self, message: types.Message):
        await message.answer(text="<b>👮‍ АДМИН ПАНЕЛЬ</b>\n\n"
                                  "________\n"
                                  f"<i>⭐️ Кол-во зарегистроированных пользователей:</i><code> {self.db.get_users_count()}</code>\n"
                                  f"<i>⭐️ Кол-во букетов в боте:</i> <code>{self.db.get_models_count()}</code>\n"
                                  f"________\n\n"
                                  f"Статистика за последние 24 часа\n\n"
                                  f"________\n"
                                  f"<i>⭐️ Кол-во зарегистроированных пользователей:</i><code>{self.db.count_users_today()}</code>\n",
                             parse_mode="HTML",
                             reply_markup=await admin_keyboard())

    @chat_id_required
    async def models(self, message: types.Message):
        await message.answer(
            text=f"📍 Управление букетами\n"
                 f"________\n"
                 f"<i>⭐️ Кол-во букетов в боте:</i> <code>{self.db.get_models_count()}</code>\n"
                 f"________\n\n"
                 f"Категории моделей\n\n"
                 f"________\n"
                 f"<i>⭐️ Кол-во категорий в боте:</i> <code>{self.db.get_categories_count()}</code>\n",
            parse_mode="HTML",
            reply_markup=await admin_models_keyboard()
        )

    @chat_id_required
    async def сategory_models(self, callback: types.CallbackQuery):
        data = self.db.select_all_categories()
        categories_text = "\n".join([f"{category[0]}. {category[1]}" for category in data])
        if not categories_text:
            categories_text = "Категории отсутствуют"
        await callback.message.answer(text=f"<b>Доступные категории моделей</b>\n\n"
                                           f"________\n"
                                           f"<i>{categories_text}</i>\n"
                                           f"________\n",
                                      parse_mode="HTML",
                                      reply_markup=await admin_models_category_keyboard())

    @chat_id_required
    async def add_category(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Введите название категории")
        await state.set_state(AddCategory.name)
        await callback.message.delete()

    @chat_id_required
    async def add_category_db(self, message: types.Message, state: FSMContext):
        await message.delete()
        await state.update_data(name=message.text)
        await message.answer("✔️ Категория успешна добавлена")
        self.db.insert_category(message.text)
        await state.clear()

    @chat_id_required
    async def delete_category(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Введите ID категории")
        await state.set_state(AddCategory.delete_name)

    @chat_id_required
    async def delete_category_name(self, message: types.Message, state: FSMContext):
        if message.text.isdigit():
            category_id = int(message.text)
            await state.update_data(delete_name=category_id)
            self.db.delete_category(category_id=category_id)
            await message.answer("✔️ Категория успешно удалена")
        else:
            await message.answer("❌ Пожалуйста, введите корректный ID категории (только число).")
            return

        await state.clear()
        await message.delete()

    @chat_id_required
    async def model(self, callback: types.CallbackQuery):
        await callback.message.edit_text(f"📍 Букеты\n\n",
                                         reply_markup=await admin_models_keyboard_add())

    @chat_id_required
    async def add_model(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text("Введите название букета")
        await state.set_state(AddModel.name_model)

    @chat_id_required
    async def add_name_model(self, message: types.Message, state: FSMContext):
        await message.delete()
        await state.update_data(name_model=message.text)
        await message.answer("Введите описание букета")
        await state.set_state(AddModel.description)

    @chat_id_required
    async def add_description_model(self, message: types.Message, state: FSMContext):
        await message.delete()
        await state.update_data(description=message.text)
        await message.answer("Введите цену букета")
        await state.set_state(AddModel.weight)

    @chat_id_required
    async def add_price_full_night_model(self, message: types.Message, state: FSMContext):
        await message.delete()
        await state.update_data(weight=message.text)
        await message.answer("Отправьте 1 фото букета")
        await state.set_state(AddModel.image)

    @chat_id_required
    async def add_image_model(self, message: types.Message, state: FSMContext):
        await message.delete()
        if not message.photo:
            await message.answer("Пожалуйста, отправьте фото.")
            return

        photo = message.photo[-1]
        file_info = await self.bot.get_file(photo.file_id)

        os.makedirs(config.token.PHOTO_DIR, exist_ok=True)

        photo_path = os.path.join(config.token.PHOTO_DIR, f"{message.from_user.id}_{photo.file_id}.jpg")

        await self.bot.download_file(file_info.file_path, photo_path)

        await state.update_data(image=photo_path)

        buttons = [[
            types.InlineKeyboardButton(text=category[1], callback_data=f'category_{category[0]}')
        ] for category in self.db.select_all_categories()]

        await message.answer("Добавьте категорию к букету",
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))

    @chat_id_required
    async def category_selected(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.delete()
        selected_category = callback.data.split('_')[1]

        await state.update_data(category=selected_category)
        cities = {
            "moskow": "Москва",
            "piter": "Санкт-Петербург",
            "kzn": "Казань",
            "samara": "Самара",
            "yfa": "Уфа",
            "perm": "Пермь",
            "volgograd": "Волгоград",
            "novosib": "Новосибирск",
            "nizhiy": "Нижний Новгород",
            "izhevsk": "Ижевск",
            "tolyati": "Тольятти",
            "habarovks": "Хабаровск",
            "tymen": "Тюмень",
            "chelny": "Набережные Челны"
        }

        buttons = [
            [types.InlineKeyboardButton(text=city_name, callback_data=f'city_{city_key}')]
            for city_key, city_name in cities.items()
        ]

        await callback.message.answer("Выберите местоположение букета",
                                      reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))

    @chat_id_required
    async def city_selected(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.delete()
        selected_key = callback.data.split('_')[1]
        cities = {
            "moskow": "Москва",
            "piter": "Санкт-Петербург",
            "kzn": "Казань",
            "samara": "Самара",
            "yfa": "Уфа",
            "perm": "Пермь",
            "volgograd": "Волгоград",
            "novosib": "Новосибирск",
            "nizhiy": "Нижний Новгород",
            "izhevsk": "Ижевск",
            "tolyati": "Тольятти",
            "habarovks": "Хабаровск",
            "tymen": "Тюмень",
            "chelny": "Набережные Челны"
        }

        selected_city = cities.get(selected_key, None)
        data = await state.get_data()

        print(data)
        self.db.add_model(
            name=data['name_model'],
            description=data['description'],
            price=data.get('weight'),
            image=data.get('image'),
            category_id=data.get('category'),
            city=selected_city
        )

        await callback.message.answer("Букет успешно добавлен!")

    @chat_id_required
    async def requisite(self, message: types.Message):
        get_requisites = self.db.get_requisites()

        requisites_dict = {
            '🇷🇺 RUB': None,
            '📱 SBP': None,
            '💶 BTC': None,
            '💲 USDT': None,
        }

        for req in get_requisites:
            method_name = req[1]
            address = req[2]
            if method_name in requisites_dict:
                requisites_dict[method_name] = address

        response_text = '<b>🗺 Доступные реквизиты на данный момент:</b>\n\n'
        has_requisites = False

        for method, address in requisites_dict.items():
            if address:
                response_text += f'• <i>{method}</i>: <code>{address}</code>\n'
                has_requisites = True
            else:
                response_text += f'• <i>{method}</i>: ❌ Не установлены\n'

        if has_requisites:
            await message.answer(response_text, reply_markup=await requisite_keyboard(),
                                 parse_mode="HTML")
        else:
            await message.answer('❗️ Реквизиты не установлены для всех методов',
                                 reply_markup=await requisite_keyboard())

    async def add_requisite(self, callback: types.CallbackQuery):
        await callback.message.edit_text('Выберите для какого метода оплаты вы хотите добавить реквизиты',
                                         reply_markup=await set_currency_admin())

    async def update_requisite(self, method, callback: types.CallbackQuery, state: FSMContext):
        print(f"Update requisite called with method: {method}")  # Логирование вызова
        await callback.message.edit_text('Напишите номер карты/кошелька')
        await state.update_data(method=method)
        await state.set_state(AddRequisite.number_card)

    @chat_id_required
    async def add_requisite_db(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        print(data)
        method = data.get('method')
        card_number = message.text

        if method and card_number:
            self.db.insert_requisite(method_name=method, address=card_number)
            await message.answer('Реквизиты успешно добавлены!', reply_markup=await admin_keyboard())
        else:
            await message.answer('Ошибка при добавлении реквизитов. Убедитесь, что все данные заполнены.')

        await state.clear()

    @chat_id_required
    async def add_number_phone(self, callback: types.CallbackQuery):
        user_id = re.search(r'ID - (\d+)', callback.message.text)
        number_order_match = re.search(r'Номер заказа - ([\w#]+)',
                                       callback.message.text)

        if user_id:
            user_id = user_id.group(1)
            print(f"Найденный ID: {user_id}")
        else:
            print("ID не найден.")

        if number_order_match:
            await callback.message.answer(text="Запрос на номер успешно отправлен")
            number_order = number_order_match.group(1)
            text = (f"<b>🧾 ВОПРОС ОТ ОПЕРАТОРОВ ПОДДЕРЖКИ ПО ЗАКАЗУ {number_order}</b>\n\n"
                    f"<i>Для подтверждения заказа необходим Ваш номер телефона</i>\n"
                    f"<i>Он будет передан нашему курьеру для дальнейшей связи с Вами</i>\n\n"
                    f"<b>🔺 Мы можем гарантировать, что Ваш номер телефона не будет нигде сохранен и передан третьем лицам</b>")
            await self.bot.send_message(user_id,
                                        text=text,
                                        parse_mode="HTML",
                                        reply_markup=await add_number_users())
        else:
            print("Номер заказа не найден.")

    async def extract_order_info(self, callback: types.CallbackQuery):
        order_number_match = re.search(r'#(\w+)', callback.message.text)
        id_match = re.search(r'ID - (\d+)', callback.message.text)

        order_number = order_number_match.group(1) if order_number_match else None
        user_id = id_match.group(1) if id_match else None

        if order_number:
            print(f"Найден номер заказа: {order_number}")
        else:
            print("Номер заказа не найден.")

        if user_id:
            print(f"Найден ID: {user_id}")
        else:
            print("ID не найден.")

        return order_number, user_id

    async def good(self, callback: types.CallbackQuery):
        order_number, user_id = await self.extract_order_info(callback)
        print(user_id)

        if order_number:
            self.db.update_order_status(order_number, "☑️ Успешно оплачено")
            text = (f"<i>🧾 Заказ {order_number} переведен во статус - ☑️ Успешно оплачено</i>\n"
                    f"<i>Ожидайте звонка от нашего оператора для уточнения деталий</i>")
            print(f"Статус заказа {order_number} обновлен на 'Успешно оплачено'.")
            await self.bot.send_message(user_id,
                                        text=text,
                                        parse_mode="HTML",
                                        reply_markup=await menu_keyboard())

            await callback.message.answer(f"<i>Заказ {order_number} переведен во статус - ☑️ Успешно оплачено</i>",
                                          parse_mode="HTML")
        else:
            print("Не удалось обновить статус заказа, номер не найден.")

    async def cancel_order(self, callback: types.CallbackQuery):
        order_number, user_id = await self.extract_order_info(callback)

        if order_number:
            self.db.update_order_status(order_number, "✖️ Заказ отменен")
            text = (f"<i>🧾 Заказ {order_number} переведен во статус - ✖️ Заказ отменен</i>\n"
                    f"<i>Ваш платеж не был найден</i>\n\n"
                    f"<b>Если Вы оплатили, то напишите в поддержку</b>")
            await self.bot.send_message(user_id,
                                        text=text,
                                        parse_mode="HTML",
                                        reply_markup=await menu_keyboard())
            print(f"Статус заказа {order_number} обновлен на 'Успешно оплачено'.")
            await callback.message.answer(f"<i>Заказ {order_number} переведен во статус - ✖️ Заказ отменен</i>",
                                          parse_mode="HTML")
        else:
            print("Не удалось обновить статус заказа, номер не найден.")

