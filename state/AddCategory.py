from aiogram.fsm.state import StatesGroup, State


class AddCategory(StatesGroup):
    name = State()
    delete_name = State()
