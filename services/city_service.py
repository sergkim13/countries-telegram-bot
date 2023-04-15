from cache.cache_module import Cache
from services.abstract_uow import AbstractUnitOfWork
from services.repositories.api.api_schemas import GeocoderSchema, WeatherSchema
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.weather import WeatherAPIRepository
from services.repositories.db.cities import CityBDRepository


class CityService(AbstractUnitOfWork):
    """
    Class for get info about city from same repositories.
    """

    def __init__(self):
        self.geocoder = GeocoderAPIRepository()
        self.crud = CityBDRepository()
        self.cache = Cache()
        self.weather_repo: WeatherAPIRepository = WeatherAPIRepository()

    async def get_city(self, name: str) -> GeocoderSchema | None:
        """
        Try to get info about city from same repositories.

        :param name: city name
        :return: information about city
        """
        city_cache = await self.cache.get_city_geocoder(name)
        if city_cache:
            return city_cache
        city_info = await self.geocoder.get_city(name)
        if city_info:
            await self.cache.set_city_geocoder(city_schema=city_info)
            return city_info

        return None

    async def get_city_weather(self, latitude: float, longitude: float) -> WeatherSchema | None:
        """
        Get temperature and feels like in city

        :param latitude: city latitude
        :param longitude: city longitude
        :return: pydantic schema with weather data
        """
        weather = await self.weather_repo.get_weather(latitude, longitude)
        return weather
