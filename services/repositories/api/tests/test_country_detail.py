import pytest

from services.repositories.api.api_schemas import CountrySchema
from services.repositories.api.country_detail import CountryAPIRepository


@pytest.mark.asyncio
async def test_get_country_detail(
        patched_country_api_repository: CountryAPIRepository, country_api_response: list) -> None:
    """
    Check normal work of get_country_detail method

    :param patched_country_api_repository: country api repository with mocked method _send_request
    :param country_api_response: normal response from currency API
    """
    response = await patched_country_api_repository.get_country_detail('RU')

    assert isinstance(response, CountrySchema), f'return invalid type: {type(response)}, expected CountrySchema'
    assert response.iso_code == country_api_response[0]['cca2']
    assert response.name == country_api_response[0]['translations']['rus']['common']
    assert response.capital == country_api_response[0]['capital'][0]
    assert response.capital_longitude == country_api_response[0]['capitalInfo']['latlng'][1]
    assert response.capital_latitude == country_api_response[0]['capitalInfo']['latlng'][0]
    assert response.area_size == country_api_response[0]['area']
    assert response.population == country_api_response[0]['population']
    assert response.currencies == {
        currency: country_api_response[0]['currencies'][currency]['name']
        for currency in country_api_response[0]['currencies']
    }
    assert response.languages == [
        language for language in country_api_response[0]['languages'].values()
    ]
