import random
import re
import string
from datetime import datetime
from aiogram.fsm.context import FSMContext

from aiogram import types, F, Bot
from aiogram import Router
from aiogram.types import FSInputFile

from keyboards.admin_keyboard.order_keyboard import order_keyboard_admin, order_keyboard_admin_1, order_keyboard_user
from keyboards.main.main_keyboards import menu_keyboard, order_keyboard
from state.SupportState import TextModel


class CatalogHandler:
    def __init__(self, db, bot_token, chat_id):
        self.router = Router()
        self.db = db
        self.register_handlers()
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    def register_handlers(self):
        self.router.callback_query(F.data.in_(['all_questionnaire', 'premium', 'massazh', 'individ', 'student']))(
            self.handle_questionnaire)
        self.router.callback_query(F.data.startswith('model_'))(self.handle_model_selection)
        self.router.callback_query(F.data.startswith('order_model_'))(self.create_order)
        self.router.callback_query(F.data.startswith('order_'))(self.process_order_selection)
        self.router.callback_query(F.data.startswith('confirm_'))(self.process_location_selection)
        self.router.callback_query(F.data.startswith('oplata_'))(self.process_oplata_selection)
        self.router.callback_query(F.data == 'add_number_phone_users')(self.add_number_phone_users)
        self.router.callback_query(F.data == 'back')(self.back)
        self.router.callback_query(F.data == 'paid')(self.paid)
        self.router.callback_query(F.data == 'cancel_order_user')(self.cancel_order)
        self.router.message(TextModel.number_phone)(self.send_number_phone_users)

    async def handle_questionnaire(self, callback: types.CallbackQuery):
        category_map = {
            'all_questionnaire': 2,
            'premium': 5,
            'massazh': 4,
            'individ': 3,
        }

        user_city = self.db.get_user_by_id(callback.from_user.id)
        print(user_city[8])
        print(category_map[callback.data])
        data = self.db.get_models_with_cities(category_map[callback.data], user_city[8])

        buttons = [
            [types.InlineKeyboardButton(text=f"{model[1]}", callback_data=f'model_{model[0]}')]
            for model in data
        ]

        if data:
            text = (f"<i>💯 В нашем боте мы гарантируем безопасность и надежность для каждого клиента</i>\n"
                    f"<i>Все букеты мы собираем лично ❤️</i>")
            await callback.message.answer(
                text=text,
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons),
                parse_mode="HTML")
        else:
            await callback.message.answer("Нет букетов в данной категории.")

    async def back(self, callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer(
            text="📍 Главное меню\n\n<i>ниже представлены доступные категории наших красивых букетов ❤️</i>",
            reply_markup=await menu_keyboard(),
            parse_mode="HTML",
        )

    async def handle_model_selection(self, callback: types.CallbackQuery):
        model_info = self.db.get_model_by_id(callback.data.split('_')[1])
        print(model_info)

        if model_info:
            response_text = (
                f"👩‍🦰 <b>🌺 Название букета: {model_info[1]}</b>\n\n"
                f"<i>💓 Описание букета: {model_info[2]}</i>\n\n"
                f"________\n"
                f"<b>💸 Цена: {model_info[3]}</b>\n\n"
                f"________\n\n"
                f"<b>❗️️Важно\n\n</b>"
                f"<b>Букет находится в городе {model_info[6]}</b>"
            )

            await callback.message.answer_photo(FSInputFile(model_info[4]),
                                                caption=response_text, parse_mode="HTML",
                                                reply_markup=await order_keyboard(model_info))
        else:
            await callback.message.answer("Модель не найдена.")

    async def create_order(self, callback: types.CallbackQuery):
        model_info = self.db.get_model_by_id(callback.data.split('_')[2])
        print(model_info)

        if model_info:
            buttons = [
                [types.InlineKeyboardButton(text=f"Самовывоз",
                                            callback_data=f"order_2h_{model_info[0]}")],
                [types.InlineKeyboardButton(text=f"Заберу из магазина",
                                            callback_data=f"order_3h_{model_info[0]}")],
            ]

            response_text = (f"<i>Отличный! </i>\n\n"
                             f"<b>Букет: {model_info[1]}</b>\n"
                             f"<i>Уточните пожалуйста как вы заберете букет</i>")

            await callback.message.answer(response_text,
                                          reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons),
                                          parse_mode="HTML")
            await callback.message.delete()

        else:
            await callback.message.answer("Модель не найдена.")

    async def process_order_selection(self, callback: types.CallbackQuery):
        data = callback.data.split('_')
        time_period = data[1]
        model_id = data[2]
        print(data, time_period, model_id)

        model_info = self.db.get_model_by_id(model_id)

        if model_info:
            response_text = f"<i>Укажите удобный метод оплаты</i>\n"

            confirm_buttons = [
                [types.InlineKeyboardButton(text="СПБ",
                                            callback_data=f"oplata_sbp_{model_id}_{time_period}")],
                [types.InlineKeyboardButton(text="По номеру карты",
                                            callback_data=f"oplata_card_{model_id}_{time_period}")],
                [types.InlineKeyboardButton(text="USDT",
                                            callback_data=f"oplata_usdt_{model_id}_{time_period}")],
                [types.InlineKeyboardButton(text="BTC",
                                            callback_data=f"oplata_btc_{model_id}_{time_period}")]
            ]

            await callback.message.edit_text(response_text,
                                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=confirm_buttons),
                                             parse_mode="HTML")
        else:
            await callback.message.answer("Модель не найдена.")

    async def process_location_selection(self, callback: types.CallbackQuery):
        data = callback.data.split('_')
        print(data)
        location = data[1]
        model_id = data[2]
        time_period = data[3]

        model_info = self.db.get_model_by_id(model_id)

        if model_info:
            selected_time = "Неизвестное время"
            price = "Неизвестная цена"
            selected_location = "Неизвестная"
            if time_period == '1h':
                selected_time = "1 час"
                price = model_info[13]
            elif time_period == '2h':
                selected_time = "Cамовывоз"
                price = model_info[3]
            elif time_period == '3h':
                selected_time = "Заберу из магазина"
                price = model_info[3]

            if location == 'home':
                selected_location = "выезд на дом"
            elif location == 'host':
                selected_location = "встреча в гостинице"

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

            response_text = (f"<b>🧾 Ваш заказ</b>\n\n"
                             f"________\n"
                             f"<i>Модель</i>: <code>{model_info[1]}</code>\n"
                             f"<i>Время:</i> <code>{selected_time}</code>\n"
                             f"<i>Локация:</i> <code>{selected_location}</code>\n"
                             f"<i>Дата создания заказа:</i> <code>{current_time}</code>\n"
                             f"________\n"
                             f"Цена: <b>{price} руб</b>\n\n"
                             f"<i>Для подверждения заказа необходимо внести предоплату в размере 50%</i>\n"
                             f"<b>Выберите удобный способ оплаты</b>")

            confirm_buttons = [
                [types.InlineKeyboardButton(text="СПБ",
                                            callback_data=f"oplata_sbp_{model_id}_{time_period}_{location}")],
                [types.InlineKeyboardButton(text="По номеру карты",
                                            callback_data=f"oplata_card_{model_id}_{time_period}_{location}")],
                [types.InlineKeyboardButton(text="USDT",
                                            callback_data=f"oplata_usdt_{model_id}_{time_period}_{location}")],
                [types.InlineKeyboardButton(text="BTC",
                                            callback_data=f"oplata_btc_{model_id}_{time_period}_{location}")]
            ]

            await callback.message.edit_text(response_text,
                                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=confirm_buttons),
                                             parse_mode="HTML")
        else:
            await callback.message.answer("Модель не найдена.")

    @staticmethod
    def generate_order_number(length=5):
        letters_and_digits = string.ascii_uppercase + string.digits
        order_number = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return order_number

    async def process_oplata_selection(self, callback: types.CallbackQuery):
        try:
            data = callback.data.split('_')
            print(f"итоговая стоимость {data}")
            if len(data) < 3:
                raise ValueError("Произошла ошибка, сделайте заказ заново")

            method = data[1]
            model_id = data[2]
            time_period = data[3]
            model_info = self.db.get_model_by_id(model_id)
            if model_info is None:
                raise ValueError("Информация о модели не найдена.")
            price = 0
            selected_time = "Неизвестное время"
            if model_info:
                price = "Неизвестная цена"
                if time_period == '1h':
                    selected_time = "1 час"
                    price = model_info[3]
                elif time_period == '2h':
                    selected_time = "Самовывоз"
                    price = model_info[3]
                elif time_period == '3h':
                    selected_time = "Заберу из магазина"
                    price = model_info[3]

            if method == "card":
                method = "🇷🇺 RUB"
            elif method == "sbp":
                method = "📱 SBP"
            elif method == "btc":
                method = "💶 BTC"
            elif method == "usdt":
                method = "💲 USDT"
            else:
                raise ValueError(f"Неверный метод оплаты: {method}")

            requisite = self.db.get_requisites_by_id(method)
            if not requisite:
                raise ValueError(f"Реквизиты для метода оплаты '{method}' не найдены.")
            order_number = self.generate_order_number()
            await callback.message.edit_text(f"<b>🧾 ЗАКАЗ #{order_number}</b>\n\n"
                                             f"<b>💵 СЧЕТ</b>\n\n"
                                             f"-------\n"
                                             f"<i>Метод оплаты:</i> <code>{method}</code>\n"
                                             f"<i>Реквизиты:</i> <code>{requisite[0][0]}</code>\n"
                                             f"<i>Сумма к оплате:</i> <code>{price}</code>\n"
                                             f"-------\n\n"
                                             f"<b>🎖 ДЕТАЛИ ЗАКАЗА</b>\n\n"
                                             f"-------\n"
                                             f"<i>Название букета:</i> <code>{model_info[1]}</code>\n"
                                             f"<i>Условия заказа:</i> <code>{selected_time}</code>\n"
                                             f"-------\n\n"
                                             f"<i>🕓 Статус заказа:</i> <code>Ожидание оплаты</code>\n\n"
                                             f"<b>Поступление и подверждение средств происходит в среднем 10 минут</b>",
                                             parse_mode="HTML",
                                             reply_markup=await order_keyboard_user())

            user_id = self.db.get_user_by_id(callback.from_user.id)
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
            if user_id is None or len(user_id) == 0:
                raise ValueError("Информация о пользователе не найдена.")
            self.db.insert_order_model_user(
                payment_id=order_number,
                user_id=user_id[0],
                model_id=model_id,
                price=price,
                status='Ожидание оплаты',
                date=formatted_date,
                method=method
            )
            text = (f"<b>🧾 Создан новый заказ</b>\n\n"
                    f"____\n"
                    f"Номер заказа - #{order_number}\n"
                    f"ID - <code>{callback.from_user.id}</code>\n"
                    f"username - <code>@{callback.from_user.username}</code>\n"
                    f"Имя - <code>{callback.from_user.first_name}</code>\n"
                    f"Фамилия - <code>{callback.from_user.last_name}</code>\n"
                    f"Сумма заказа - <code>{price}</code>\n"
                    f"Выбранный метод оплаты - <code>{method}</code>\n"
                    f"Дата создания заявки - <code>{formatted_date}</code>\n"
                    f"____")

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode="HTML",
                reply_markup=await order_keyboard_admin()
            )

        except ValueError as ve:
            await callback.message.answer(f"Ошибка: {str(ve)}")
            print(f"Ошибка: {ve}")

        except Exception as e:
            await callback.message.answer("Произошла ошибка при обработке вашего выбора. Попробуйте еще раз.")
            print(f"Произошла ошибка: {e}")

    @staticmethod
    async def add_number_phone_users(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text("<i>Введите Ваш номер телефона</i>", parse_mode="HTML")
        match = re.search(r'#(\w+)', callback.message.text)
        if match:
            order_number = match.group(0)
            await state.update_data(order_number=order_number)
            print(f"Найденный номер заказа: {order_number}")
        else:
            print("Номер заказа не найден.")
        await state.set_state(TextModel.number_phone)

    async def send_number_phone_users(self, message: types.Message, state: FSMContext):
        user_input = message.text
        if self.validate_phone_number(user_input):
            await message.delete()
            await message.answer("<i>🟢 Ваш номер телефона успешно отправлен нашим оператам</i>\n\n"
                                 "<b>🕙 Ожидайте звонка нашей модели для уточнения деталий</b>",
                                 parse_mode="HTML")
            data = await state.get_data()
            text = (f"<b>НОВОЕ СООБЩЕНИЕ ПО ЗАКАЗУ {data.get('order_number')}</b>\n\n"
                    f"<i>Пользователь @{message.from_user.username} передал номер телефона</i> - <code>{user_input}</code>\n\n"
                    f"ID - {message.from_user.id}")
            await self.bot.send_message(self.chat_id,
                                        text=text,
                                        reply_markup=await order_keyboard_admin_1(),
                                        parse_mode="HTML")
            await state.clear()
        else:
            await message.answer(
                "Некорректный номер телефона. Пожалуйста, введите номер в формате +7 (XXX) XXX-XX-XX.")
            await state.set_state(TextModel.number_phone)

    @staticmethod
    def validate_phone_number(phone_number):
        cleaned_number = re.sub(r'\D', '', phone_number)

        pattern = r'^7\d{10}$'

        if re.match(pattern, cleaned_number):
            return cleaned_number
        else:
            return False

    async def paid(self, callback: types.CallbackQuery):
        match = re.search(r'ЗАКАЗ #(\w+)', callback.message.text)
        if match:
            order = match.group(1)
            self.db.update_order_status(order,
                                        "🕓 Платеж проверяется")
            await callback.message.answer(text=f"<i>ЗАКАЗ #{order} переведен в статус - 🕓 Платеж проверяется</i>\n\n"
                                               f"<b>Ожидайте подверждение платежа от операторов</b>",
                                          reply_markup=await menu_keyboard(),
                                          parse_mode="HTML")
            await self.bot.send_message(self.chat_id,
                                        text=f"ЗАКАЗ #{order} переведен в статус - 🕓 Платеж проверяется\n\n"
                                             f"<b>Проверьте пополнение счета</b>\n"
                                             f"USERNAME - {callback.from_user.username}"
                                             f"ID - {callback.from_user.id}",
                                        reply_markup=await order_keyboard_admin_1(),
                                        parse_mode="HTML")

    async def cancel_order(self, callback: types.CallbackQuery):
        match = re.search(r'ЗАКАЗ #(\w+)', callback.message.text)
        if match:
            order = match.group(1)
            self.db.update_order_status(order,
                                        "⛔️ Заказ отменен")
            await callback.message.answer(text=f"<i>ЗАКАЗ #{order} переведен в статус - ⛔️ Заказ отменен</i>\n\n",
                                          reply_markup=await menu_keyboard(),
                                          parse_mode="HTML")
            await self.bot.send_message(self.chat_id,
                                        text=f"ЗАКАЗ #{order} переведен в статус - ⛔️ Заказ отменен\n\n"
                                             f"USERNAME - {callback.from_user.username}",
                                        parse_mode="HTML")
