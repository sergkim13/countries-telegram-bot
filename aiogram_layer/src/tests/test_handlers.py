import pytest
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.types import InlineKeyboardMarkup

from aiogram_layer.src.callbacks import Callbacks as cb
from aiogram_layer.src.keyboards import main_menu, to_main_menu
from aiogram_layer.src.messages import ABOUT_MESSAGE, ENTER_CITY, INVALID_CITY
from aiogram_layer.src.states import Form
from aiogram_layer.src.tests.cases import (
    test_choose_city_from_list_cases,
    test_process_city_name_cases,
    test_start_page_cases,
)
from aiogram_layer.src.tests.fixtures import get_callback_query, get_message, get_update


@pytest.mark.asyncio
@pytest.mark.parametrize('command, state, state_data, answer, markup', test_start_page_cases)
async def test_start_page(command: str, state: FSMContext, state_data: dict, answer: str, markup: InlineKeyboardMarkup,
                          dispatcher: Dispatcher, bot: Bot):
    message = get_message(text=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=message))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup


@pytest.mark.asyncio
@pytest.mark.parametrize('command, state, state_data, answer, markup',
                         [(str(cb.about.value), None, None, ABOUT_MESSAGE, main_menu)])
async def test_show_about_page(command: str, state: FSMContext, state_data: dict, answer: str,
                               markup: InlineKeyboardMarkup, dispatcher: Dispatcher, bot: Bot):
    call = get_callback_query(query=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(call=call))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup


@pytest.mark.asyncio
@pytest.mark.parametrize('command, state, state_data, answer, markup',
                         [(str(cb.city.value), None, None, ENTER_CITY, to_main_menu)])
async def test_enter_city_name(command: str, state: FSMContext, state_data: dict, answer: str,
                               markup: InlineKeyboardMarkup, dispatcher: Dispatcher, bot: Bot):
    call = get_callback_query(query=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(call=call))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup


@pytest.mark.asyncio
@pytest.mark.parametrize('command, state, state_data, answer, markup',
                         [('131', Form.city_search, None, INVALID_CITY, to_main_menu)])
async def test_process_city_name_invalid(command: str, state: FSMContext, state_data: dict, answer: str,
                                         markup: InlineKeyboardMarkup, dispatcher: Dispatcher, bot: Bot):
    message = get_message(text=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=message))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup


@pytest.mark.asyncio
@pytest.mark.django_db
@pytest.mark.parametrize('command, state, state_data, answer, markup', test_process_city_name_cases)
async def test_process_city_name(command: str, state: FSMContext, state_data: dict, answer: str,
                                 markup: InlineKeyboardMarkup, dispatcher: Dispatcher, bot: Bot):
    message = get_message(text=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=message))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup


@pytest.mark.asyncio
@pytest.mark.django_db
@pytest.mark.parametrize('command, state, state_data, answer, markup', test_choose_city_from_list_cases)
async def test_choose_city_from_list(command: str, state: FSMContext, state_data: dict, answer: str,
                                     markup: InlineKeyboardMarkup, dispatcher: Dispatcher, bot: Bot):
    call = get_callback_query(query=command)
    result = await dispatcher.feed_update(bot=bot, update=get_update(call=call))

    assert isinstance(result, SendMessage)
    assert result.text == answer
    assert result.reply_markup == markup
