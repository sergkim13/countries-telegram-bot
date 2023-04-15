import pytest
from pytest_asyncio import fixture as async_fixture

from cache.cache_module import Cache
from cache.test.fixtures import CITY_COORDINATES_KEY, COUNTRY_COORDINATES_KEY


class TestCacheCity:
    """
    Cache city repository test.
    All tests are atomic.
    """
    @pytest.mark.asyncio
    async def test_get_city_none(
        self,
        _clear_cache_city: async_fixture,
    ) -> None:
        """
        Trying to get a non-existent city cache.
        """
        assert await Cache.get_city(CITY_COORDINATES_KEY) is None

    @pytest.mark.asyncio
    async def test_create_city(
        self,
        _clear_cache_city: async_fixture,
        city_data: async_fixture
    ) -> None:
        """
        Test for creating a city entry in the cache.
        """
        await Cache.create_or_update_city(city_data)
        assert await Cache.get_city(f'{city_data.longitude}_{city_data.latitude}') == city_data

    @pytest.mark.asyncio
    async def test_get_city(
        self,
        _clear_cache_city: async_fixture,
        _create_cache_city: async_fixture,
        city_data: async_fixture,
    ) -> None:
        """
        Test for getting an existing city entry in the cache.
        """
        assert await Cache.get_city(CITY_COORDINATES_KEY) == city_data


class TestCacheCountry:
    """
    Cache city repository test.
    All tests are atomic.
    """
    @pytest.mark.asyncio
    async def test_get_country_none(
        self,
        _clear_cache_country: async_fixture
    ) -> None:
        """
        Trying to get a non-existent country cache.
        """
        assert await Cache.get_country(COUNTRY_COORDINATES_KEY) is None

    @pytest.mark.asyncio
    async def test_create_country(
        self,
        _clear_cache_country: async_fixture,
        country_data: async_fixture,
    ) -> None:
        """
        Test for creating a country entry in the cache.
        """
        assert await Cache.get_country(COUNTRY_COORDINATES_KEY) is None
        await Cache.create_or_update_country(COUNTRY_COORDINATES_KEY, country_data)
        assert await Cache.get_country(COUNTRY_COORDINATES_KEY) == country_data

    @pytest.mark.asyncio
    async def test_get_country(
        self,
        _create_cache_country: async_fixture,
        country_data: async_fixture,
    ) -> None:
        """
        Test for getting an existing country entry in the cache.
        """
        assert await Cache.get_country(COUNTRY_COORDINATES_KEY) == country_data
