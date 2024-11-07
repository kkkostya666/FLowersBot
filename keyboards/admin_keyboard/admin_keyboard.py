from aiogram import types


async def admin_models_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Категории букетов",
                    callback_data="category_model"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Букеты",
                    callback_data="model"
                )
            ],
        ]
    )


async def admin_models_keyboard_add():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Добавить букет",
                    callback_data="add_model"
                )
            ],
        ]
    )


async def admin_models_category_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Добавить новую категорию",
                    callback_data="add_category"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Удалить категорию",
                    callback_data="delete_category"
                )
            ],
        ]
    )


async def admin_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="👧 Управление букетами"),
            ],
            [
                types.KeyboardButton(text="🔎 РАССЫЛКА")
            ],
            [
                types.KeyboardButton(text="🛠️ Управление реквизитами"),

            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def requisite_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Добавить реквизиты",
                    callback_data="add_requisite"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Удалить реквизиты",
                    callback_data="delete_requisite"
                )
            ],
        ]
    )