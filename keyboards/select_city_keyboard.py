from aiogram import types


async def set_sity():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="МОСКВА",
                    callback_data="moskow"
                ),
                types.InlineKeyboardButton(
                    text="САНКТ ПЕТЕРБУРГ",
                    callback_data="piter"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="КАЗАНЬ",
                    callback_data="kzn"
                ),
                types.InlineKeyboardButton(
                    text="САМАРА",
                    callback_data="samara"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="УФА",
                    callback_data="yfa"
                ),
                types.InlineKeyboardButton(
                    text="НИЖНИЙ НОВГОРОД",
                    callback_data="nizhiy"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="ХАБАРОВСК",
                    callback_data="habarovks"
                ),
                types.InlineKeyboardButton(
                    text="НАБЕРЕЖНЫЕ ЧЕЛНЫ",
                    callback_data="chelny"
                )
            ],
        ]
    )


async def set_sity_update():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="МОСКВА",
                    callback_data="moskow_update"
                ),
                types.InlineKeyboardButton(
                    text="САНКТ ПЕТЕРБУРГ",
                    callback_data="piter_update"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="КАЗАНЬ",
                    callback_data="kzn_update"
                ),
                types.InlineKeyboardButton(
                    text="САМАРА",
                    callback_data="samara_update"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="УФА",
                    callback_data="yfa_update"
                ),
                types.InlineKeyboardButton(
                    text="НИЖНИЙ НОВГОРОД",
                    callback_data="nizhiy_update"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="ХАБАРОВСК",
                    callback_data="habarovks_update"
                ),
                types.InlineKeyboardButton(
                    text="НАБЕРЕЖНЫЕ ЧЕЛНЫ",
                    callback_data="chelny_update"
                )
            ],
        ]
    )
