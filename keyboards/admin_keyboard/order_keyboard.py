from aiogram import types


async def order_keyboard_admin():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Запросить номер телефона",
                    callback_data="add_number_phone"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Оплачено",
                    callback_data="good"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Отклонить заявку",
                    callback_data="cancel_order"
                )
            ],
        ]
    )


async def add_number_users():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отправить номер телефона",
                    callback_data="add_number_phone_users"
                ),
            ],
        ]
    )


async def order_keyboard_admin_1():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Оплачено",
                    callback_data="good"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Отклонить заявку",
                    callback_data="cancel_order"
                )
            ],
        ]
    )

async def order_keyboard_user():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🟡 Оплатил",
                    callback_data="paid"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="⛔️ Отменить",
                    callback_data="cancel_order_user"
                )
            ],
        ]
    )