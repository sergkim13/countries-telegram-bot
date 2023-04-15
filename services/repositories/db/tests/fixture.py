import pytest
import pytest_asyncio

from django_layer.countries_app.models import City, Country
from services.repositories.api.api_schemas import CitySchema, CountrySchema


@pytest.fixture
def test_city_data() -> CitySchema:
    return CitySchema(
        name='Moscow',
        country_code='RU',
        longitude=37.61,
        latitude=55.75,
        is_capital=True,
    )


@pytest.fixture
def updated_test_city_data() -> CitySchema:
    return CitySchema(
        name='Saint Petersburg',
        country_code='RU',
        longitude=37.61,
        latitude=55.75,
        is_capital=False,
    )


@pytest_asyncio.fixture
async def country_fixture():
    country = await Country.objects.acreate(
        iso_code='RU',
        name='The Russian Federation',
        population=143000000,
        area_size=17100000,
    )
    return country


@pytest_asyncio.fixture
async def city_fixture(country_fixture, test_city_data):
    city = await City.objects.acreate(
        name=test_city_data.name,
        longitude=test_city_data.longitude,
        latitude=test_city_data.latitude,
        is_capital=test_city_data.is_capital,
        country=await Country.objects.aget(iso_code=test_city_data.country_code),
    )
    return city


@pytest_asyncio.fixture
def test_updated_country_data() -> CountrySchema:
    """
    The fixture to create filled CountrySchema for testing countries db repository

    :return: CountrySchema
    """
    return CountrySchema(
        iso_code='RU',
        name='Россия',
        capital='Москва',
        capital_longitude=37.6,
        capital_latitude=55.75,
        population=333333333,
        area_size=9999999,
        currencies={'RUB': 'Russian ruble', 'USD': 'Dollar'},
        languages=['Русский']
    )


@pytest_asyncio.fixture
async def db_country(country_data: CountrySchema) -> Country:
    """
    The fixture to create Country record in the test database
    Creates linked capital, languages, currencies in database

    :param country_data: CountrySchema

    :return: Country object
    """
    country = await Country.objects.acreate(
        iso_code=country_data.iso_code,
        name=country_data.name,
        population=country_data.population,
        area_size=country_data.area_size
    )
    await City.objects.acreate(
        name=country_data.capital,
        longitude=country_data.capital_longitude,
        latitude=country_data.capital_latitude,
        is_capital=True,
        country=country
    )
    for language in country_data.languages:
        await country.languages.acreate(name=language)
    for iso_code, currency_name in country_data.currencies.items():
        await country.currencies.acreate(iso_code=iso_code, name=currency_name)

    return country
