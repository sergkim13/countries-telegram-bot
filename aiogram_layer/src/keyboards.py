from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_layer.src.buttons import Buttons
from aiogram_layer.src.callbacks import CitiesCB

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.country_search.value],
        [Buttons.city_search.value],
        [Buttons.about.value],
    ]
)
weather_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.country.value],
        [Buttons.currency.value],
        [Buttons.to_main_menu.value],
    ]
)
country_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.currency.value],
        [Buttons.to_main_menu.value],
    ]
)
city_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.currency.value],
        [Buttons.country.value],
        [Buttons.to_main_menu.value],
    ]
)
currency_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.weather.value],
        [Buttons.country.value],
        [Buttons.to_main_menu.value],
    ]
)
to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [Buttons.to_main_menu.value],
    ]
)


async def create_cities_list_markup(city_info):
    builder = InlineKeyboardBuilder()
    for city in city_info:
        builder.button(text=city.full_address, callback_data=CitiesCB(coordinates=city.coordinates))
    builder.adjust(1, True)
    return builder
