import pytest

from services.repositories.api.api_schemas import WeatherSchema
from services.repositories.api.weather import WeatherAPIRepository, WeatherType


@pytest.mark.asyncio
async def test_get_weather(patched_weather_api_repository: WeatherAPIRepository, weather_api_response: dict) -> None:
    """
    Check normal work of get_weather method

    :param patched_weather_api_repository: weather api repository with mocked method _send_request
    :param weather_api_response: expected response from weather API
    """

    response = await patched_weather_api_repository.get_weather(latitude=11, longitude=22)
    main = weather_api_response['main']

    assert isinstance(response, WeatherSchema), f'return invalid type: {type(response)}, expected WeatherSchema'
    assert response.temperature == round(main['temp'], 1)
    assert response.temperature_feels_like == round(main['feels_like'], 1)
    assert response.weather_type == getattr(WeatherType, weather_api_response['weather'][0]['main'])
    assert response.humidity == main['humidity']
    assert response.max_temperature == round(main['temp_max'], 1)
    assert response.min_temperature == round(main['temp_min'], 1)
    assert response.wind_speed == weather_api_response['wind']['speed']
