import asyncio
from dataclasses import dataclass

from pydantic.error_wrappers import ValidationError

from cache.cache_module import Cache
from django_layer.countries_app.models import Country
from services.abstract_uow import AbstractUnitOfWork
from services.repositories.api.api_schemas import (
    CountrySchema,
    CurrencySchema,
    GeocoderSchema,
    WeatherSchema,
)
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.countries import CountryDBRepository
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema
from services.service_schemas import CityCoordinatesSchema, CountryUOWSchema


@dataclass
class CountryService(AbstractUnitOfWork):
    """
    Class to get info about country from cache, database and api repositories.
    """
    cache: Cache = Cache()
    geocoder: GeocoderAPIRepository = GeocoderAPIRepository()
    countries_repo: CountryAPIRepository = CountryAPIRepository()
    weather_repo: WeatherAPIRepository = WeatherAPIRepository()
    currency_repo: CurrencyAPIRepository = CurrencyAPIRepository()
    crud: CountryDBRepository = CountryDBRepository()

    async def get_country_info(self, country_name: str) -> GeocoderSchema | None:
        """
        Try to get info about country from cache or :class:`GeocoderAPIRepository`.

        :param country_name: country name

        :return: information about country as :class:`GeocoderSchema` object
        """
        country_cache = await self.cache.get_country_by_name(country_name)
        if country_cache:
            return country_cache
        country_info = await self.geocoder.get_country(country_name)
        if country_info:
            await self.cache.set_country_geocoder(country_info)
        return country_info

    async def get_country_all_info(self, country_info: GeocoderSchema) -> CountryUOWSchema | None:
        """
        Collects all information about country: country details, capital, languages, currecnies.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: all information about country as :class:`CountryUOWSchema` object
        """
        detail = await self.get_country(country_info)
        languages_task = asyncio.create_task(self.get_languages(country_info))
        currencies_task = asyncio.create_task(self.get_currencies(country_info))
        capital_task = asyncio.create_task(self.get_capital_info(country_info))
        languages, currencies, capital = await asyncio.gather(languages_task, currencies_task, capital_task)
        try:
            return CountryUOWSchema(
                detail=detail, languages=languages, currencies=currencies, capital=capital)
        except ValidationError:
            return None

    async def get_country(self, country_info: GeocoderSchema) -> CountrySchema | Country | None:
        """
        Collects detailed information about country from cache or database.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: detailed information about country as :class:`CountrySchema` object or Country object
        """
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return cache_country
        db_country = await self.crud.get_by_pk(country_info.country_code)
        if not db_country:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            if country:
                db_country = await self._create_db_and_cache_country(country, country_info.coordinates)
        return db_country

    async def get_languages(self, country_info: GeocoderSchema) -> LanguageNamesSchema | None:
        """
        Collects information about country languages from cache or database.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: country languages as :class:`LanguageNamesSchema` object
        """
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return LanguageNamesSchema(languages=cache_country.languages)
        languages = await self.crud.get_country_languages(country_info.country_code)
        if not languages:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            if country:
                db_country = await self._create_db_and_cache_country(country, country_info.coordinates)
                languages = await self.crud.get_country_languages(db_country.iso_code)
        return languages

    async def get_currencies(self, country_info: GeocoderSchema) -> CurrencyCodesSchema | None:
        """
        Collects information about country currencies from cache or database.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: country currencies as :class:`CurrencyCodesSchema` object
        """
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CurrencyCodesSchema(currency_codes=[currency for currency in cache_country.currencies.keys()])
        currencies = await self.crud.get_country_currencies(country_info.country_code)
        if not currencies:
            country = await self.countries_repo.get_country_detail(country_info.country_code)
            if country:
                db_country = await self._create_db_and_cache_country(country, country_info.coordinates)
                currencies = await self.crud.get_country_currencies(db_country.iso_code)
        return currencies

    async def get_capital_info(self, country_info: GeocoderSchema) -> CityCoordinatesSchema | None:
        """
        Collects information about country capital from cache or database.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: country capital as :class:`CityCoordinatesSchema` object
        """
        cache_country = await self.cache.get_country(country_info.coordinates)
        if cache_country:
            return CityCoordinatesSchema(
                name=cache_country.capital,
                latitude=cache_country.capital_latitude,
                longitude=cache_country.capital_longitude,
            )
        city = await self.crud.get_capital(country_info.country_code)
        if city:
            return CityCoordinatesSchema(
                name=city.name,
                latitude=city.latitude,
                longitude=city.longitude,
            )
        return None

    async def get_currency_rates(self, currencies: CurrencyCodesSchema) -> list[CurrencySchema] | None:
        """
        Returns information about rates of currencies used in the country.

        :param currencies: country currencies as :class:`CurrencyCodesSchema` object

        :return: list of :class:`CurrencySchema` object or None
        """
        return await self.currency_repo.get_rate(currencies.currency_codes)

    async def get_capital_weather(self, country_info: GeocoderSchema) -> WeatherSchema | None:
        """
        Returns information about weather in the country capital.

        :param country_info: information about country as :class:`GeocoderSchema` object

        :return: capital weather as :class:`WeatherSchema` object or None
        """
        city = await self.get_capital_info(country_info)
        if city:
            return await self.weather_repo.get_weather(city.latitude, city.longitude)
        return None

    async def _create_db_and_cache_country(self, country: CountrySchema, coordinates: str) -> Country:
        """
        Create new country record in database and cache.

        :param country: information about country as :class:`GeocoderSchema` object
        :param coordinates: coordinates of a country

        :return: Country object
        """
        db_country = await self.crud.create(country)
        updated_country = await self.crud.update_country_schema(country, db_country)
        await self.cache.create_or_update_country(coordinates, updated_country)
        return db_country
