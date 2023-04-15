import pytest
from asgiref.sync import sync_to_async

from cache.cache_module import Cache
from cache.test.fixtures import COUNTRY_NAME
from django_layer.countries_app.models import City, Country
from services.country_service import CountryService
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema
from services.service_schemas import CityCoordinatesSchema, CountryUOWSchema


@pytest.mark.asyncio
async def test_get_country_info_from_api_and_create_in_cache(
        expected_geocoder_country_result, patched_geocoder_api_repository_for_country):
    cached_country = await Cache().get_country_by_name(COUNTRY_NAME)

    assert cached_country is None

    country_info = await CountryService(
        geocoder=patched_geocoder_api_repository_for_country).get_country_info(COUNTRY_NAME)
    cached_country = await Cache().get_country_by_name(COUNTRY_NAME)

    assert country_info == expected_geocoder_country_result
    assert cached_country == expected_geocoder_country_result


@pytest.mark.asyncio
async def test_get_country_info_from_cache(
        expected_geocoder_country_result,
        _create_cache_country_by_name, patched_geocoder_api_repository_for_country):
    cached_country = await Cache().get_country_by_name(COUNTRY_NAME)
    country_info = await CountryService(
        geocoder=patched_geocoder_api_repository_for_country).get_country_info(COUNTRY_NAME)

    assert cached_country == country_info
    assert country_info == expected_geocoder_country_result


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_from_cache(
    patched_country_api_repository,
    expected_geocoder_country_result, _create_cache_country
):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    country = await CountryService(
        countries_repo=patched_country_api_repository).get_country(expected_geocoder_country_result)

    assert cached_country == country


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_from_db(
        expected_geocoder_country_result,
        db_country, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 1

    country = await CountryService(
        countries_repo=patched_country_api_repository).get_country(expected_geocoder_country_result)

    assert country == db_country


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_country_from_api_and_create_in_db_and_cache(
        country_data, expected_geocoder_country_result, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 0

    country = await CountryService(
        countries_repo=patched_country_api_repository).get_country(expected_geocoder_country_result)
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)

    assert await sync_to_async(countries.count)() == 1
    assert cached_country == country_data
    assert country.pk == country_data.iso_code


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_languages_from_cache(
    patched_country_api_repository,
    expected_geocoder_country_result, _create_cache_country
):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    languages = await CountryService(
        countries_repo=patched_country_api_repository).get_languages(expected_geocoder_country_result)

    assert LanguageNamesSchema(languages=cached_country.languages) == languages


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_languages_from_db(
        db_country, country_data,
        expected_geocoder_country_result, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 1

    languages = await CountryService(
        countries_repo=patched_country_api_repository).get_languages(expected_geocoder_country_result)
    expected = LanguageNamesSchema(languages=country_data.languages)

    assert languages == expected


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_new_country_and_get_languages_from_db(
        country_data, expected_geocoder_country_result, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 0

    languages = await CountryService(
        countries_repo=patched_country_api_repository).get_languages(expected_geocoder_country_result)
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)

    assert await sync_to_async(countries.count)() == 1

    db_country = await Country.objects.afirst()
    db_languages = [language.name async for language in await sync_to_async(db_country.languages.all)()]

    assert cached_country.languages == country_data.languages
    assert languages.languages == db_languages


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_currencies_from_cache(
    patched_country_api_repository,
    expected_geocoder_country_result, _create_cache_country
):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    currencies = await CountryService(
        countries_repo=patched_country_api_repository).get_currencies(expected_geocoder_country_result)

    assert CurrencyCodesSchema(currency_codes=[currency for currency in cached_country.currencies.keys()]) == currencies


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_currencies_from_db(
        db_country, country_data,
        expected_geocoder_country_result, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 1

    currencies = await CountryService(
        countries_repo=patched_country_api_repository).get_currencies(expected_geocoder_country_result)
    expected = CurrencyCodesSchema(currency_codes=[currency for currency in country_data.currencies])

    assert currencies == expected


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_new_country_and_get_currencies_from_db(
        country_data, expected_geocoder_country_result, patched_country_api_repository):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 0

    currencies = await CountryService(
        countries_repo=patched_country_api_repository).get_currencies(expected_geocoder_country_result)
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)

    assert await sync_to_async(countries.count)() == 1

    db_country = await Country.objects.afirst()
    db_currencies = [currency.iso_code async for currency in await sync_to_async(db_country.currencies.all)()]

    assert cached_country.languages == country_data.languages
    assert currencies.currency_codes == db_currencies


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_capital_info_from_cache(
    expected_geocoder_country_result, _create_cache_country
):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    capital_info = await CountryService().get_capital_info(expected_geocoder_country_result)
    expected = CityCoordinatesSchema(
        name=cached_country.capital,
        latitude=cached_country.capital_latitude,
        longitude=cached_country.capital_longitude,
    )

    assert capital_info == expected


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_capital_info_from_db(db_country, expected_geocoder_country_result):
    cached_country = await Cache().get_country(expected_geocoder_country_result.coordinates)
    countries = await sync_to_async(Country.objects.all)()

    assert cached_country is None
    assert await sync_to_async(countries.count)() == 1

    db_capital = await City.objects.afirst()
    capital_info = await CountryService().get_capital_info(expected_geocoder_country_result)
    expected = CityCoordinatesSchema(
        name=db_capital.name,
        latitude=db_capital.latitude,
        longitude=db_capital.longitude,
    )

    assert capital_info == expected


@pytest.mark.asyncio
async def test_get_country_all_info_from_cache(expected_geocoder_country_result, _create_cache_country):
    country_info = await CountryService().get_country_all_info(expected_geocoder_country_result)
    detail = await Cache().get_country(expected_geocoder_country_result.coordinates)
    expected = CountryUOWSchema(
        detail=detail,
        languages=LanguageNamesSchema(languages=[language for language in detail.languages]),
        currencies=CurrencyCodesSchema(currency_codes=[currency for currency in detail.currencies.keys()]),
        capital=CityCoordinatesSchema(name=detail.capital, latitude=detail.capital_latitude,
                                      longitude=detail.capital_longitude,)
    )
    assert country_info == expected
