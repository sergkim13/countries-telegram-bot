import pytest

from services.repositories.api.api_schemas import GeocoderSchema
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.tests.cases import get_fixed_request_name_cases


@pytest.mark.asyncio
async def test_get_country(
    patched_geocoder_api_repository_for_country: GeocoderAPIRepository,
    expected_geocoder_country_result: GeocoderSchema,
) -> None:
    """
    Check normal work of `get_country` method

    :param patched_geocoder_api_repository_for_country: geocoder api repository with mocked method `_send_request`
    which returns country result
    :param expected_geocoder_country_result: expected response from geocoder API with country result
    """

    response = await patched_geocoder_api_repository_for_country.get_country(country_name='Росия')

    assert isinstance(response, GeocoderSchema), f'return invalid type: {type(response)}, expected `GeocoderSchema`'
    assert response == expected_geocoder_country_result


@pytest.mark.asyncio
async def test_get_city(
    patched_geocoder_api_repository_for_city: GeocoderAPIRepository,
    expected_geocoder_city_result: list[GeocoderSchema],
) -> None:
    """
    Check normal work of `get_city` method

    :param patched_geocoder_api_repository_for_city: geocoder api repository with mocked method `_send_request`
    which returns city result
    :param expected_geocoder_city_result: expected response from geocoder API with city result
    """

    response = await patched_geocoder_api_repository_for_city.get_city(city_name='Гурьевск')

    assert isinstance(response, list), f'return invalid type: {type(response)}, expected `list`'
    for object in response:
        assert isinstance(object, GeocoderSchema), f'return invalid type: {type(response)}, expected `GeocoderSchema`'
    assert response == expected_geocoder_city_result


@pytest.mark.asyncio
async def test_get_country_or_city_not_found(
    patched_geocoder_api_repository_not_found: GeocoderAPIRepository,
) -> None:
    """
    Check work of `get_country` and `get_city` method with `None` result

    :param patched_geocoder_api_repository_not_found: geocoder api repository with mocked method `_send_request`
    which returns no result
    """

    response_country = await patched_geocoder_api_repository_not_found.get_country(country_name='1')
    response_city = await patched_geocoder_api_repository_not_found.get_city(city_name='1')

    assert response_country is None
    assert response_city is None


@pytest.mark.asyncio
@pytest.mark.parametrize('test_cases, expected', get_fixed_request_name_cases)
async def test_parse_fixed_request_name(test_cases: list, expected: list) -> None:
    """
    Check normal work of `parse_fixed_request_name` method

    :param test_cases: test input data for `parse_fixed_request_name` method
    :param expected: test expected results for `parse_fixed_request_name` method
    """
    geocoder_api_repository = GeocoderAPIRepository()
    response = await geocoder_api_repository.parse_fixed_request_name(test_cases)
    assert response == expected
