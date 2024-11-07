from aiogram import types


async def set_currency():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🇷🇺 RUB",
                    callback_data="RUB"
                ),
                types.InlineKeyboardButton(
                    text="📱 SPB",
                    callback_data="sbp"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="💲 USDT",
                    callback_data="usdt"
                ),
                types.InlineKeyboardButton(
                    text="💶 BTC",
                    callback_data="btc"
                )
            ]]
    )


async def set_currency_admin():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🇷🇺 RUB",
                    callback_data="RUB_admin"
                ),
                types.InlineKeyboardButton(
                    text="📱 SPB",
                    callback_data="sbp_admin"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="💲 USDT",
                    callback_data="usdt_admin"
                ),
                types.InlineKeyboardButton(
                    text="💶 BTC",
                    callback_data="btc_admin"
                )
            ]]
    )
