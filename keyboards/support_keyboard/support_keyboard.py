from aiogram import types


async def support_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🦋 Ответить",
                    callback_data="support_send"
                ),
            ],
            # [
            #     types.InlineKeyboardButton(
            #         text="Отправить стандартный ответ",
            #         callback_data="standart"
            #     ),
            # ],
        ]
    )
