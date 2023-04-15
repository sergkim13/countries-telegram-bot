import pytest

from aiogram_layer.src.tests.cases import (
    is_city_name_valid_cases,
    is_country_name_valid_cases,
)
from aiogram_layer.src.validators import is_city_name_valid, is_country_name_valid


@pytest.mark.asyncio
@pytest.mark.parametrize('city_name, expected', is_city_name_valid_cases)
async def test_is_city_name_valid(city_name: str, expected: bool) -> None:
    """
        Check normal work of is_city_name_valid function

        :param city_name: city name
        :param expected: expected result of function
    """

    is_valid = is_city_name_valid(city_name)
    assert is_valid == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('country_name, expected', is_country_name_valid_cases)
async def test_is_country_name_valid(country_name: str, expected: bool) -> None:
    """
        Check normal work of is_city_name_valid function

        :param country_name: country name
        :param expected: expected result of function
    """

    is_valid = is_country_name_valid(country_name)
    assert is_valid == expected
