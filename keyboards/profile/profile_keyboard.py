from aiogram import types


async def profile_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🗄 Мои заказы",
                    callback_data="my_zakaz"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="💵 Смена валюты",
                    callback_data="change_currency"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="🌎 Смена города",
                    callback_data="change_city"
                )
            ],
        ]
    )