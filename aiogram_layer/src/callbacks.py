from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Callbacks(Enum):
    country = 'country'
    city = 'city'
    about = 'about'
    to_main_menu = 'to_main_menu'
    weather = 'weather'
    country_info = 'country_info'
    currency_rate = 'currency_rate'


class CitiesCB(CallbackData, prefix='city'):  # type: ignore
    coordinates: str
