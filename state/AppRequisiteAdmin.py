from aiogram.fsm.state import StatesGroup, State


class AddRequisite(StatesGroup):
    number_card = State()
