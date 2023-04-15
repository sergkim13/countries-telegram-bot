from aiogram import types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from aiogram_layer.src.app import dp
from aiogram_layer.src.callbacks import Callbacks as cb
from aiogram_layer.src.callbacks import CitiesCB
from aiogram_layer.src.keyboards import (
    city_detail,
    country_detail,
    create_cities_list_markup,
    currency_detail,
    main_menu,
    to_main_menu,
    weather_detail,
)
from aiogram_layer.src.messages import (
    ABOUT_MESSAGE,
    CITIES_LIST,
    CITY_NOT_FOUND,
    COUNTRY_NOT_FOUND,
    COUNTRY_UNAVAILABLE,
    CURRENCIES_UNAVAILABLE,
    ENTER_CITY,
    ENTER_COUNTRY,
    INVALID_CITY,
    INVALID_COUNTRY,
    NON_TRADING_CURRENCY,
    RESTART_MESSAGE,
    START_MESSAGE,
    UNKNOWN_COMMAND,
    WEATHER_NOT_AVAILABLE,
    get_capital_weather_text,
    get_city_info_text,
    get_city_weather_text,
    get_country_info_text,
    get_currency_rate_text,
)
from aiogram_layer.src.states import CountryCityForm, Form
from aiogram_layer.src.validators import is_city_name_valid, is_country_name_valid
from services.city_service import CityService
from services.country_service import CountryService


@dp.message(Command('start', 'help'))
async def start_page(message: types.Message):
    """
    This handler will be called when user sends /start or /help command

    :param message: message

    :return: main menu
    """
    return await message.answer(
        text=START_MESSAGE,
        reply_markup=main_menu
    )


@dp.callback_query(Text(cb.about.value))
async def show_about_page(callback: types.CallbackQuery):
    """
    This handler will be called when user chooses 'О проекте' in main menu.
    Shows info about bot's features.

    :param callback: callback function
    :type callback: types.CallbackQuery

    :return: basic info about project
    """
    return await callback.message.reply(
        text=ABOUT_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query(Text(cb.city.value))
async def enter_city_name(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Поиск по городу' in main menu.

    :param state: current state
    :param callback: callback function

    :return: dialogue for enter city name
    """
    await state.set_state(Form.city_search)
    await callback.message.delete()
    return await callback.message.answer(
        text=ENTER_CITY,
        reply_markup=to_main_menu
    )


@dp.message(lambda message: not is_city_name_valid(message.text), Form.city_search)
async def process_city_name_invalid(message: types.Message):
    """
    This handler will be called when user input invalid city name.

    :param message: message

    :return: warning message about invalid city name
    """
    return await message.reply(
        text=INVALID_CITY,
        reply_markup=to_main_menu
    )


@dp.message(Form.city_search)
async def process_city_name(message: types.Message, state: FSMContext):
    """
    This handler will be called when user inputs city name.
    Continues the dialogue about the country where the city is located.

    :param message: user's message
    :param state: state

    :return: City info or list of cities if city name occurs several times
    """
    async with CityService() as uow:
        city_info = await uow.get_city(message.text)
    if not city_info:
        return await message.reply(
            text=CITY_NOT_FOUND,
            reply_markup=to_main_menu
        )

    if isinstance(city_info, list):
        builder = await create_cities_list_markup(city_info)
        await state.update_data(data={city.coordinates: city for city in city_info})

        return await message.answer(
            text=CITIES_LIST,
            reply_markup=builder.as_markup()
        )
    async with CountryService() as uow:
        country_all_info = await uow.get_country_all_info(city_info)
        await state.update_data(
            city_info=city_info,
            country_detail=country_all_info,
        )
    text = get_city_info_text(city_info)
    return await message.answer(
        text=text,
        reply_markup=city_detail,
    )


@dp.callback_query(CitiesCB.filter(), Form.city_search)
async def choose_city_from_list(callback: types.CallbackQuery, callback_data: CitiesCB, state: FSMContext):
    """
    This handler works if city name entered by user occurs several times and user chose one

    :param callback:
    :param callback_data:
    :param state:
    :return: city info
    """
    data = await state.get_data()
    city_info = data[callback_data.coordinates]
    async with CountryService() as uow:
        country_all_info = await uow.get_country_all_info(city_info)
        await state.update_data(
            city_info=city_info,
            country_detail=country_all_info,
        )
    text = get_city_info_text(city_info)
    return await callback.message.answer(
        text=text,
        reply_markup=city_detail,
    )


@dp.callback_query(Text(cb.weather.value), CountryCityForm().city_search)
async def get_city_weather(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.

    :param callback: callback function
    :param state: state

    :return: info about temperature and feels like in city
    """

    async with CityService() as uow:
        data = await state.get_data()
        city_info = data['city_info']
        long, lat = city_info.coordinates.split()
        weather = await uow.get_city_weather(float(lat), float(long))
    text = get_city_weather_text(city_info, weather)

    return await callback.message.answer(
        text=text,
        reply_markup=weather_detail,
    )


@dp.callback_query(
    Text(cb.weather.value),
    Form.country_search
)
async def get_capital_weather(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Погода' button.
    Continues the dialog about weather details.

    :param callback: callback function
    :type callback: types.CallbackQuery
    :param state: state
    :type state: FSMContext

    :return: info about weather in capital of country
    """
    detail_text = WEATHER_NOT_AVAILABLE
    data = await state.get_data()
    async with CountryService() as uow:
        weather = await uow.get_capital_weather(data['country_info'])
    if weather:
        detail_text = get_capital_weather_text(weather)
    return await callback.message.answer(
        text=detail_text,
        reply_markup=weather_detail,
    )


@dp.callback_query(
    Text(cb.country_info.value),
    CountryCityForm()
)
async def get_country_info(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Подробнее о стране' button.
    Continues the dialog about country details.

    :param state: state
    :param callback: callback function

    :return: info about country
    """
    data = await state.get_data()
    if not data['country_detail']:
        return await callback.message.reply(
            text=COUNTRY_UNAVAILABLE,
            reply_markup=country_detail
        )
    country_all_info = data['country_detail']
    text = get_country_info_text(country_all_info)
    return await callback.message.answer(
        text=text,
        reply_markup=country_detail,
    )


@dp.callback_query(
    Text(cb.currency_rate.value),
    CountryCityForm()
)
async def get_currency_rate(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Курс валюты' button.
    Continues the dialog about currency rate.
    :param state: state
    :param callback: callback function

    :return: currency rate: national currency/ruble
    """
    data = await state.get_data()
    if not data['country_detail']:
        return await callback.message.answer(
            text=CURRENCIES_UNAVAILABLE,
            reply_markup=currency_detail
        )
    async with CountryService() as uow:
        currencies = await uow.get_currency_rates(data['country_detail'].currencies)
    if not currencies:
        return await callback.message.answer(
            text=NON_TRADING_CURRENCY,
            reply_markup=currency_detail,
        )
    text = get_currency_rate_text(currencies)
    return await callback.message.answer(
        text=text,
        reply_markup=currency_detail,
    )


@dp.callback_query(Text(cb.to_main_menu.value))
async def return_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'К началу' button.
    Resets all states, restarts dialog.

    :param callback: callback function
    :param state: state

    :return: Main menu
    """
    await state.clear()
    return await callback.message.reply(
        text=RESTART_MESSAGE,
        reply_markup=main_menu,
    )


@dp.callback_query(Text(cb.country.value))
async def enter_country_name(callback: types.CallbackQuery, state: FSMContext):
    """
    This handler will be called when user chooses 'Поиск по стране'.

    :param state: state None
    :param callback: arg1

    :return: dialogue for enter country name
    """
    await state.set_state(Form.country_search)
    return await callback.message.reply(
        text=ENTER_COUNTRY,
        reply_markup=to_main_menu,
    )


@dp.message(lambda message: not is_country_name_valid(message.text), Form.country_search)
async def process_country_name_invalid(message: types.Message):
    """
    This handler will be called when user input invalid country name.

    :param message: message

    :return: warning message about invalid country name
    """
    return await message.reply(
        text=INVALID_COUNTRY,
        reply_markup=to_main_menu,
    )


@dp.message(Form.country_search)
async def process_country_name(message: types.Message, state: FSMContext):
    """
    This handler will be called when user inputs country name.

    :param state: state
    :param message: arg1

    :return: info about country
    """
    async with CountryService() as uow:
        info = await uow.get_country_info(message.text)
        if not info:
            return await message.reply(
                text=COUNTRY_NOT_FOUND,
                reply_markup=to_main_menu,
            )
        country_all_info = await uow.get_country_all_info(info)
        if not country_all_info:
            return await message.reply(
                text=COUNTRY_UNAVAILABLE,
                reply_markup=to_main_menu,
            )
    await state.update_data(
        country_info=info,
        country_detail=country_all_info
    )
    text = get_country_info_text(country_all_info)
    return await message.answer(
        text=text,
        reply_markup=country_detail,
    )


@dp.message()
async def handle_unknown_commands(message: types.Message):
    """
    This handler for handling unknown commands

    :param message: message

    :return: warning message with instructions
    """
    return message.reply(
        text=UNKNOWN_COMMAND,
        reply_markup=to_main_menu,
    )
