from aiogram.fsm.state import StatesGroup, State


class AddModel(StatesGroup):
    name_model = State()
    description = State()
    weight = State()
    bust_size = State()
    height = State()
    age = State()
    clothing_size = State()
    boots_size = State()
    color_hair = State()
    appearance = State()
    physique = State()
    price_four = State()
    price_two_four = State()
    price_full_night = State()
    image = State()
    city = State()