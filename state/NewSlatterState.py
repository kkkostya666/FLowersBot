from aiogram.fsm.state import StatesGroup, State


class NewSlatter(StatesGroup):
    text = State()