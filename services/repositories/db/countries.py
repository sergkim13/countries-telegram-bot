from asgiref.sync import sync_to_async
from django.utils import translation
from django.utils.translation import gettext

from django_layer.countries_app.models import City, Country, Currency, Language
from services.repositories.api.country_detail import CountrySchema
from services.repositories.db.abstract_db_repository import AbstractDBRepository
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema


class CountryDBRepository(AbstractDBRepository):
    """
    This is a class of a Country Database repository. Provides CRUD operations for Country entity.
    Supported methods: create, update, get_by_pk, get_by_name, get_capital, get_country_currencies, get_country_languages.
    Extends of the :class:`AbstractDBRepository` class.
    """
    async def create(self, data: CountrySchema) -> Country:
        """
        Create a country record in Country table.

        :param data: new country attributed as :class:`CountrySchema` object

        :return: created country record from Country table
        """
        new_country = await Country.objects.acreate(
            iso_code=data.iso_code,
            name=data.name,
            area_size=data.area_size,
            population=data.population
        )
        await self._set_languages(data.languages, new_country)
        await self._set_currencies(data.currencies, new_country)
        await self._create_capital_city(data)
        return new_country

    async def update(self, data: CountrySchema) -> Country:
        """
        Update a country record in Country table.

        :param iso_code: country database identificator
        :param data: city attributes to update as :class:`CountrySchema` object

        :return: created country record from Country table
        """
        country, created = await Country.objects.aupdate_or_create(
            iso_code=data.iso_code,
            defaults={
                'name': data.name,
                'area_size': data.area_size,
                'population': data.population
            }
        )
        await self._update_capital_city(data)
        await self._update_languages(data.languages, country)
        await self._update_currencies(data.currencies, country)
        return country

    async def get_by_pk(self, iso_code: str) -> Country | None:
        """
        Looking for country record with requested iso_code.
        Returns a country record from Country table or None, if not found.

        :param iso_code: country database identificator

        :return: country record from Country table or None
        """
        try:
            country = await Country.objects.aget(pk=iso_code)
            return country
        except Country.DoesNotExist:
            return None

    async def get_by_name(self, name: str) -> Country | None:
        """
        Looking for country record with requested name.
        Returns a country record from Country table or None, if not found.

        :param name: country name in russian

        :return: country record from Country table or None
        """
        try:
            country = await Country.objects.aget(name=name)
            return country
        except Country.DoesNotExist:
            return None

    async def get_capital(self, country_pk: str) -> City | None:
        """
        Looking for city record with requested country pk.
        Returns a city record from City table or None, if not found.

        :param country_pk: country database identificator

        :return: city record from City table or None
        """
        try:
            city = await City.objects.filter(country_id=country_pk).aget(is_capital=True)
            return city
        except City.DoesNotExist:
            return None

    async def update_country_schema(self, country: CountrySchema, db_country: Country) -> CountrySchema:
        """
        Updates CountrySchema with localised languages of country, created in database.

        :param country: CountrySchema
        param db_country: Country object

        :return: CountrySchema
        """
        country.languages = [language.name async for language in await sync_to_async(db_country.languages.all)()]
        return country

    async def get_country_currencies(self, country_pk: str) -> CurrencyCodesSchema | None:
        """
        Looking for all currency records with requested country pk.
        Returns a list of currency names from Currency table or None, if not found.

        :param country_pk: country database identificator

        :return: list of currency names from Currency table or None
        """
        country = await self.get_by_pk(country_pk)
        if country:
            currencies = [currency.iso_code async for currency in await sync_to_async(country.currencies.all)()]
            return CurrencyCodesSchema(currency_codes=currencies)
        return None

    async def get_country_languages(self, country_pk: str) -> LanguageNamesSchema | None:
        """
        Looking for all language records with requested country pk.
        Returns a list of languages names from Language table or None, if not found.

        :param country_pk: country database identificator

        :return: list of language names from Language table or None
        """
        country = await self.get_by_pk(country_pk)
        if country:
            languages = [language.name async for language in await sync_to_async(country.languages.all)()]
            return LanguageNamesSchema(languages=languages)
        return None

    async def _set_languages(self, languages: list, country: Country) -> None:
        """
        Create new languages for concrete country in database or sets existing language for country.

        :param languages: list of languages (example: ["English", "French"])
        :param country: Country object

        :return: None
        """
        translation.activate('ru')
        languages = [gettext(language) for language in languages]
        translation.deactivate()
        filtered_languages = await sync_to_async(Language.objects.filter)(name__in=languages)
        existing_languages = [language async for language in await sync_to_async(filtered_languages.all)()]
        languages = [
            language for language in languages if language not in [
                language.name for language in existing_languages
            ]
        ]
        new_languages = [Language(name=language) for language in languages]
        await self._bulk_create_languages(country, new_languages, existing_languages)

    async def _set_currencies(self, currencies: dict, country: Country) -> None:
        """
        Create new currencies for concrete country in database or sets existing currencies for country.

        :param currencies: dict of currencies (example: {"CAN": "Canadian dollar", "EUR": "Euro"})
        :param country: Country object

        :return: None
        """
        filtered_currencies = await sync_to_async(Currency.objects.filter)(iso_code__in=currencies.keys())
        existing_currencies = [currency async for currency in await sync_to_async(filtered_currencies.all)()]
        currencies = {
            code: name for code, name in currencies.items() if code not in [
                currency.iso_code for currency in existing_currencies
            ]
        }
        new_currencies = [Currency(iso_code=code, name=currency) for code, currency in currencies.items()]
        await self._bulk_create_currencies(country, new_currencies, existing_currencies)

    async def _update_languages(self, languages: list, country: Country) -> None:
        """
        Update languages for concrete country in database.

        :param languages: list of languages (example: ["English", "French"])
        :param country: Country object

        :return: None
        """
        await sync_to_async(country.languages.clear)()
        translation.activate('ru')
        languages = [gettext(language) for language in languages]
        translation.deactivate()
        await self._set_languages(languages, country)

    async def _update_currencies(self, currencies: dict, country: Country) -> None:
        """
        Update currencies for concrete country in database.

        :param currencies: dict of currencies (example: {"CAN": "Canadian dollar", "EUR": "Euro"})
        :param country: Country object

        :return: None
        """
        for code, name in currencies.items():
            await Currency.objects.filter(iso_code=code).aupdate_or_create(iso_code=code,
                                                                           defaults={'name': name})
        await sync_to_async(country.currencies.clear)()
        existing_currencies = [Currency(iso_code=code, name=name) for code, name in currencies.items()]
        await self._bulk_create_currencies(country, existing_currencies=existing_currencies)

    @staticmethod
    async def _bulk_create_languages(
        country: Country, new_languages: list = [], existing_languages: list = []
    ) -> None:
        """
        Inserts the provided list of languages for concrete country into the database.
        Creates links between country and languages (new and existing) in the database.

        :param country: Country object
        :param new_languages: list of new Language objects to insert into the database
        :param existing_languages: list of existing Language objects to create links with country in the database

        :return: None
        """
        if new_languages:
            await country.languages.abulk_create(new_languages)
            existing_languages += new_languages
        languages_to_country_links = [(Country.languages.through(
            country_id=country.pk, language_id=language.pk)) for language in existing_languages]
        await country.languages.through.objects.abulk_create(languages_to_country_links)

    @staticmethod
    async def _bulk_create_currencies(
        country: Country, new_currencies: list = [], existing_currencies: list = []
    ) -> None:
        """
        Inserts the provided list of currencies for concrete country into the database.
        Creates links between country and currencies (new and existing) in the database.

        :param country: Country object
        :param new_currencies: list of new Currency objects to insert into the database
        :param existing_currencies: list of existing Currency objects to create links with country in the database

        :return: None
        """
        if new_currencies:
            await country.currencies.abulk_create(new_currencies)
            existing_currencies += new_currencies
        currencies_to_country_links = [(Country.currencies.through(
            country_id=country.pk, currency_id=currency.pk)) for currency in existing_currencies]
        await country.currencies.through.objects.abulk_create(currencies_to_country_links)

    @staticmethod
    async def _create_capital_city(data: CountrySchema) -> City:
        """
        Create a capital city record in City table

        :param data: new country attributed as :class:`CountrySchema` object

        :return: created city record from City table
        """
        new_city = await City.objects.acreate(
            name=data.capital,
            longitude=data.capital_longitude,
            latitude=data.capital_latitude,
            is_capital=True,
            country=await Country.objects.aget(iso_code=data.iso_code)
        )
        return new_city

    @staticmethod
    async def _update_capital_city(data: CountrySchema) -> None:
        """
        Update a capital city record in City table

        :param data: new country attributed as :class:`CountrySchema` object

        :return: None
        """
        await City.objects.filter(country_id=data.iso_code, is_capital=True).aupdate(
            name=data.capital
        )


def get_country_db_repository() -> CountryDBRepository:
    """
    Returns object of :class:`CountryDBRepository` class

    return: :class:`CountryDBRepository` object
    """
    return CountryDBRepository()
