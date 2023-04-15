import locale

from services.repositories.api.api_schemas import (
    CurrencySchema,
    GeocoderSchema,
    WeatherSchema,
)
from services.service_schemas import CountryUOWSchema

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

START_MESSAGE = '''
Привет! Выберите, что Вас интересует:
'''
RESTART_MESSAGE = '''
Выберите, что Вас интересует:
'''
ABOUT_MESSAGE = '''
*Данный бот позволяет получить информацию о любой стране*:
-площадь\n-численность населения\n-официальные языки\n-курс местной валюты к рублю\n-погоду в столице\n
Также можно ввести название города и узнать погоду в данном городе.
'''
ENTER_CITY = '''
Введите название городa:
'''
ENTER_COUNTRY = '''
Введите название страны:
'''
COUNTRY_INFO = '''
Информация о стране *{country}*:

Столица: {capital}
Население: {population:n} человек
Площадь территории: {area:n} км²
Государственный язык: {languages}
Государственная валюта: {currencies}
'''
CITY_INFO = '''
Информация о городe: *{city}*

Полный адрес: {full_address}
Координаты(долгота, широта): {coordinates}
'''
CITY_NOT_FOUND = '''
Город с таким названием не найден
'''
WEATHER_DETAIL = '''
Погода в городе *{city}*:

Тип погоды: {weather_type}
Температура: {temperature}°C
Ощущается как: {feels_like}°C
Максимальная температура: {max_temperature}°C
Минимальная температура: {min_temperature}°C
Влажность: {humidity}%
Скорость ветра: {wind_speed} м/с
'''
WEATHER_DETAIL_COUNTRY = '''
Погода в столице:

Тип погоды: {weather_type}
Температура: {temperature}°C
Ощущается как: {feels_like}°C
Максимальная температура: {max_temperature}°C
Минимальная температура: {min_temperature}°C
Влажность: {humidity}%
Скорость ветра: {wind_speed} м/с
'''
CURRENCY_RATE_DETAIL = '''
Курс валют к рублю: {currency_details}
'''
INVALID_CITY = '''
Неверное название города. Попробуйте еще раз
'''
INVALID_COUNTRY = '''
Неверное название страны. Попробуйте еще раз
'''
COUNTRY_NOT_FOUND = '''
Такая страна не найдена. Попробуйте еще раз
'''
NON_TRADING_CURRENCY = '''
Валюта страны не торгуется к рублю
'''
CITIES_LIST = '''
По указанному названию нашлось несколько вариантов:
'''
WEATHER_NOT_AVAILABLE = '''
Извините, информация о погоде сейчас недоступна
'''
COUNTRY_UNAVAILABLE = '''
Извините, информация о странах сейчас недоступна
'''
CURRENCIES_UNAVAILABLE = '''
Извините, информация о курсах валют сейчас недоступна
'''
UNKNOWN_COMMAND = '''
'Неизвестная команда.\nДля перехода в главное меню используйте команду: /start'
'''


def get_city_info_text(city_info: GeocoderSchema) -> str:
    return CITY_INFO.format(
        city=city_info.name.capitalize(),
        full_address=city_info.full_address,
        coordinates=city_info.coordinates,
    )


def get_country_info_text(country_all_info: CountryUOWSchema) -> str:
    return COUNTRY_INFO.format(
        country=country_all_info.detail.name,
        capital=country_all_info.capital.name,
        population=country_all_info.detail.population,
        area=country_all_info.detail.area_size,
        languages=', '.join(str(language) for language in country_all_info.languages.languages),
        currencies=', '.join(str(currency) for currency in country_all_info.currencies.currency_codes),
    )


def get_currency_rate_text(currencies: list[CurrencySchema]) -> str:
    currency_details = ', '.join(
        f'Валюта: {currency.name}\nКурс: {currency.value} RUB/{currency.char_code}' for currency in currencies
    )

    return currency_details
    # return CURRENCY_RATE_DETAIL.format(currency_details=currency_details)


def get_city_weather_text(city_info: GeocoderSchema, weather: WeatherSchema):
    return WEATHER_DETAIL.format(
        city=city_info.name.capitalize(),
        feels_like=weather.temperature_feels_like,
        temperature=weather.temperature,
        weather_type=weather.weather_type,
        max_temperature=weather.max_temperature,
        min_temperature=weather.min_temperature,
        humidity=weather.humidity,
        wind_speed=weather.wind_speed,
    )


def get_capital_weather_text(weather: WeatherSchema):
    return WEATHER_DETAIL_COUNTRY.format(
        feels_like=weather.temperature_feels_like,
        temperature=weather.temperature,
        weather_type=weather.weather_type,
        max_temperature=weather.max_temperature,
        min_temperature=weather.min_temperature,
        humidity=weather.humidity,
        wind_speed=weather.wind_speed,
    )
