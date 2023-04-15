import pytest
from asgiref.sync import sync_to_async

from django_layer.countries_app.models import City, Country
from services.repositories.db.countries import CountryDBRepository
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_country_create(country_data):
    """
    Check normal work of `create` method

    :param country_data: new country attributes

    :return: None
    """
    countries = await sync_to_async(Country.objects.all)()
    assert await sync_to_async(countries.count)() == 0

    country = await CountryDBRepository().create(country_data)
    capital = await City.objects.aget(country_id=country.iso_code, is_capital=True)
    languages = [
        language.name async for language in await sync_to_async(country.languages.all)()
    ]
    currencies = {
        currency.iso_code: currency.name async for currency in await sync_to_async(country.currencies.all)()
    }

    assert await sync_to_async(countries.count)() == 1
    assert country.iso_code == country_data.iso_code
    assert country.name == country_data.name
    assert country.population == country_data.population
    assert country.area_size == country_data.area_size
    assert capital.name == country_data.capital
    assert capital.longitude == country_data.capital_longitude
    assert capital.latitude == country_data.capital_latitude
    assert capital.is_capital is True
    assert languages == country_data.languages
    assert currencies == country_data.currencies


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_country_update(db_country, test_updated_country_data):
    """
    Check normal work of `update` method

    :param db_country: fixture which inserts country into database
    :param test_updated_country_data: country attributes to update

    :return: None
    """
    countries = await sync_to_async(Country.objects.all)()
    assert await sync_to_async(countries.count)() == 1

    country = await CountryDBRepository().update(test_updated_country_data)
    capital = await City.objects.aget(country_id=country.iso_code, is_capital=True)
    languages = [
        language.name async for language in await sync_to_async(country.languages.all)()
    ]
    currencies = {
        currency.iso_code: currency.name async for currency in await sync_to_async(country.currencies.all)()
    }

    assert await sync_to_async(countries.count)() == 1
    assert country.iso_code == test_updated_country_data.iso_code
    assert country.name == test_updated_country_data.name
    assert country.population == test_updated_country_data.population
    assert country.area_size == test_updated_country_data.area_size
    assert capital.name == test_updated_country_data.capital
    assert capital.longitude == test_updated_country_data.capital_longitude
    assert capital.latitude == test_updated_country_data.capital_latitude
    assert capital.is_capital is True
    assert languages == test_updated_country_data.languages
    assert currencies == test_updated_country_data.currencies


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_by_pk_not_found():
    """
    Check normal work of `get_country_by_pk` method when required country doesn't exist in database

    :return: None
    """
    country = await CountryDBRepository().get_by_pk('non_existing_code')
    assert country is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_by_pk(db_country):
    """
    Check normal work of `get_country_by_pk` method

    :param db_country: fixture which inserts country into database

    :return: None
    """
    country = await CountryDBRepository().get_by_pk(db_country.iso_code)
    assert country == db_country


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_by_name_not_found():
    """
    Check normal work of `get_country_by_name` method when required country doesn't exist in database

    :return: None
    """
    country = await CountryDBRepository().get_by_name('non_existing_country')
    assert country is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_by_name(db_country):
    """
    Check normal work of `get_country_by_name` method

    :param db_country: fixture which inserts country into database

    :return: None
    """
    country = await CountryDBRepository().get_by_name(db_country.name)
    assert country == db_country


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_capital_not_found():
    """
    Check normal work of `get_capital` method when required country doesn't exist in database

    :return: None
    """
    capital = await CountryDBRepository().get_capital('non_existing_code')
    assert capital is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_capital(db_country, country_data):
    """
    Check normal work of `get_capital` method

    :param db_country: fixture which inserts country into database
    :param test_country_data: country attributes

    :return: None
    """
    capital = await CountryDBRepository().get_capital(country_data.iso_code)
    assert capital.name == country_data.capital
    assert capital.longitude == country_data.capital_longitude
    assert capital.latitude == country_data.capital_latitude
    assert capital.is_capital is True


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_languages_not_found():
    """
    Check normal work of `get_country_languages` method when required country doesn't exist in database

    :return: None
    """
    languages = await CountryDBRepository().get_country_languages('non_existing_code')
    assert languages is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_languages(db_country, country_data):
    """
    Check normal work of `get_country_languages` method

    :param db_country: fixture which inserts country into database
    :param test_country_data: country attributes

    :return: None
    """
    languages = await CountryDBRepository().get_country_languages(country_data.iso_code)
    expected = LanguageNamesSchema(languages=country_data.languages)
    assert languages == expected


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_currencies_not_found():
    """
    Check normal work of `get_country_currencies` method when required country doesn't exist in database

    :return: None
    """
    currencies = await CountryDBRepository().get_country_currencies('non_existing_code')
    assert currencies is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_currencies(db_country, country_data):
    """
    Check normal work of `get_country_languages` method

    :param db_country: fixture which inserts country into database
    :param test_country_data: country attributes

    :return: None
    """
    currencies = await CountryDBRepository().get_country_currencies(country_data.iso_code)
    expected = CurrencyCodesSchema(currency_codes=[name for name in (country_data.currencies).keys()])
    assert currencies == expected
