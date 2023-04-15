from aiogram.fsm.state import State, StatesGroup


class CountryCityForm(StatesGroup):
    """
    The Form for saving dialog states in the storage
    """
    country_search = State()
    city_search = State()


class Form(CountryCityForm):
    pass
