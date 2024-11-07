from aiogram import types


async def autorizate_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="АВТОРИЗИРОВАТЬСЯ",
                    callback_data="autorizate"
                ),
                types.InlineKeyboardButton(
                    text="ЗАРЕГИСТРИРОВАТЬСЯ",
                    callback_data="register"
                )
            ]]
    )


async def only_register():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="ЗАРЕГИСТРИРОВАТЬСЯ",
                    callback_data="register"
                )
            ]]
    )


async def only_autorizate():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="АВТОРИЗИРОВАТЬСЯ",
                    callback_data="autorizate"
                ),
            ]]
    )


# async def only_register_1():
#     # Создаем обычную клавиатуру для регистрации
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=[
#             [types.KeyboardButton("ЗАРЕГИСТРИРОВАТЬСЯ")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#     return keyboard


async def reply_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="♻️ ГЛАВНОЕ МЕНЮ"),
            ],
            [
                types.KeyboardButton(text="👤 ПРОФИЛЬ"),
            ],
            [
                types.KeyboardButton(text="🛠️ ТЕХНИЧЕСКАЯ ПОДДЕРЖКА")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
