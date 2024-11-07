from aiogram.fsm.state import StatesGroup, State


class TextModel(StatesGroup):
    text = State()
    text_support = State()
    user_id = State()
    number_phone = State()