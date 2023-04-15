from django_layer.countries_app.models import City, Country
from services.repositories.api.api_schemas import CitySchema
from services.repositories.db.abstract_db_repository import AbstractDBRepository


class CityBDRepository(AbstractDBRepository):
    """
    This is a class of a CitiesRepository repository. Provides CRUD operations for City entity.
    Supported methods: create, update, get_by_pk, get_by_name.
    Extends of the :class:`AbstractDBRepository` class.
    """

    async def get_by_pk(self, city_id: int) -> City | None:
        """
        Looking for city record with requested id.
        Returns a city record from City table.

        :param city_id: city database identificator

        :return: city record from City tables
        """
        try:
            city = await City.objects.select_related('country').aget(id=city_id)
            return city
        except City.DoesNotExist:
            return None

    async def get_by_name(self, city_name: str) -> City | None:
        """
        Looking for city record with requested name.
        Returns a city record from City table.

        :param city_name: city name

        :return: city record from City table.
        """
        try:
            city = await City.objects.select_related('country').aget(name=city_name)
            return city
        except City.DoesNotExist:
            return None

    async def create(self, data: CitySchema) -> City:
        """
        Create a city record in City table

        :param data: new city attributes

        :return: created city record from City table
        """
        new_city = await City.objects.acreate(
            name=data.name,
            longitude=data.longitude,
            latitude=data.latitude,
            is_capital=data.is_capital,
            country=await Country.objects.aget(iso_code=data.country_code)
        )
        return new_city

    async def update(self, city_id: int, data: CitySchema) -> City:
        """
        Update a city record in City table

        :param city_id: city database identificator
        :param data: city attributes to update

        :return: updated city record from City table
        """
        updated_city, _ = await City.objects.aupdate_or_create(
            id=city_id,
            defaults={
                'name': data.name,
                'longitude': data.longitude,
                'latitude': data.latitude,
                'is_capital': data.is_capital,
                'country': await Country.objects.aget(iso_code=data.country_code)
            }
        )
        return updated_city


def get_cities_repository() -> CityBDRepository:
    """
    Returns object of :class:`CitiesRerpository` class

    return: :class:`CitiesRerpository` object
    """
    return CityBDRepository()
