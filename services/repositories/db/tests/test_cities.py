import pytest

from services.repositories.api.api_schemas import CitySchema
from services.repositories.db.cities import CityBDRepository


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_city_by_pk(city_fixture):
    """
    Check normal work of `get_city_by_pk`

    :param city_fixture: fixture which insert city into database
    """
    city_repository = CityBDRepository()
    city = await city_repository.get_by_pk(city_id=1)
    assert city == city_fixture


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_city_by_name(city_fixture):
    """
    Check normal work of `get_city_by_name` method

    :param city_fixture: fixture which insert city into database
    """
    city_repository = CityBDRepository()
    city = await city_repository.get_by_name(city_name='Moscow')
    assert city == city_fixture


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_city_by_pk_not_found():
    """
    Check work of `get_city_by_pk` method when required city doesn't exist in database
    """
    city_repository = CityBDRepository()
    city = await city_repository.get_by_pk(city_id=-999)
    assert city is None


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_city_by_name_not_found():
    """
    Check work of `get_city_by_name` method when required city doesn't exist in database
    """
    city_repository = CityBDRepository()
    city = await city_repository.get_by_name(city_name='not_existing_city')
    assert city is None


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_city(country_fixture, test_city_data: CitySchema):
    """
    Check work of `create` method when required city doesn't exist in database

    :param country_fixture: fixture which insert country into database
    :param test_city_data: new city attributes
    """
    city_repository = CityBDRepository()
    created_city = await city_repository.create(test_city_data)
    assert created_city.name == test_city_data.name
    assert created_city.country.iso_code == test_city_data.country_code
    assert created_city.latitude == test_city_data.latitude
    assert created_city.longitude == test_city_data.longitude
    assert created_city.is_capital == test_city_data.is_capital


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_update_city(city_fixture, updated_test_city_data: CitySchema):
    """
    Check work of `update` method when required city doesn't exist in database

    :param city_fixture: fixture which insert city into database
    :param updated_test_city_data: city attributes to update
    """
    city_repository = CityBDRepository()
    updated_city = await city_repository.update(city_id=city_fixture.id, data=updated_test_city_data)
    assert updated_city.id == city_fixture.id
    assert updated_city.name == updated_test_city_data.name
    assert updated_city.latitude == updated_test_city_data.latitude
    assert updated_city.longitude == updated_test_city_data.longitude
    assert updated_city.is_capital == updated_test_city_data.is_capital
