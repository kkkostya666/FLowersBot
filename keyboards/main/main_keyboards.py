from aiogram import types


async def menu_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🦋 Классические круглые",
                    callback_data="all_questionnaire"
                ),
                types.InlineKeyboardButton(
                    text="🍑 Микс",
                    callback_data="individ"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="👸 Каркасные",
                    callback_data="premium"
                ),
                types.InlineKeyboardButton(
                    text="💆 Корзинки",
                    callback_data="massazh"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="💌 Написать в поддержку",
                    callback_data="support"
                ),
            ],
        ]
    )


async def order_keyboard(model_info):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="💶 Оформить заказ",
                    callback_data=f"order_model_{model_info[0]}"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data="back"
                )
            ],
        ]
    )
