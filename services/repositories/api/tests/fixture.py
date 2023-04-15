import json
from http import HTTPStatus

import pytest_asyncio
from pytest import MonkeyPatch

from services.repositories.api.api_schemas import GeocoderSchema
from services.repositories.api.country_detail import CountryAPIRepository
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.geocoder import GeocoderAPIRepository
from services.repositories.api.tests.mocks import MockClientResponse
from services.repositories.api.weather import WeatherAPIRepository


@pytest_asyncio.fixture
async def patched_currency_api_repository(monkeypatch: MonkeyPatch, currency_api_response: dict):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param currency_api_response: normal response from currency API

    :return: patched CurrencyAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(currency_api_response), HTTPStatus.OK)

    currency_api_repository = CurrencyAPIRepository()
    monkeypatch.setattr(currency_api_repository, '_send_request', return_mock)

    yield currency_api_repository


@pytest_asyncio.fixture
async def currency_api_response() -> dict:
    return {
        'Date': '2023-03-17T11:30:00+03:00',
                'PreviousDate': '2023-03-16T11:30:00+03:00',
                'PreviousURL': r'\/\/www.cbr-xml-daily.ru\/archive\/2023\/03\/16\/daily_json.js',
                'Timestamp': '2023-03-16T17:00:00+03:00',
                'Valute': {
                    'AUD': {
                        'ID': 'R01010',
                        'NumCode': '036',
                        'CharCode': 'AUD',
                        'Nominal': 1,
                        'Name': 'Австралийский доллар',
                        'Value': 50.713,
                        'Previous': 50.689
                    },
                    'USD': {
                        'ID': 'R01235',
                        'NumCode': '840',
                        'CharCode': 'USD',
                        'Nominal': 1,
                        'Name': 'Доллар США',
                        'Value': 76.4096,
                        'Previous': 75.7457
                    },
                }}


@pytest_asyncio.fixture
async def patched_weather_api_repository(monkeypatch: MonkeyPatch, weather_api_response: dict):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param weather_api_response: expected response from weather API

    :return: patched WeatherAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(weather_api_response), HTTPStatus.OK)

    weather_api_repository = WeatherAPIRepository()
    monkeypatch.setattr(weather_api_repository, '_send_request', return_mock)

    yield weather_api_repository


@pytest_asyncio.fixture
def weather_api_response() -> dict:
    return {
        'base': 'stations',
        'clouds': {'all': 100},
        'cod': 200,
        'coord': {'lat': 55.75, 'lon': 37.61},
        'dt': 1679039854,
        'id': 524901,
        'main': {'feels_like': -1.58,
                 'grnd_level': 1007,
                 'humidity': 94,
                 'pressure': 1025,
                 'sea_level': 1025,
                 'temp': 2.34,
                 'temp_max': 3.06,
                 'temp_min': 1.31},
        'name': 'Moscow',
        'sys': {'country': 'RU',
                'id': 2000314,
                'sunrise': 1679024464,
                'sunset': 1679067308,
                'type': 2},
        'timezone': 10800,
        'visibility': 10000,
        'weather': [{'description': 'overcast clouds',
                    'icon': '04d',
                     'id': 804,
                     'main': 'Clouds'}],
        'wind': {'deg': 12, 'gust': 10.4, 'speed': 4.28}
    }


@pytest_asyncio.fixture
async def patched_country_api_repository(monkeypatch: MonkeyPatch, country_api_response: list):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param currency_api_response: normal response from country API

    :return: patched CountryAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(country_api_response), HTTPStatus.OK)

    country_api_repository = CountryAPIRepository()
    monkeypatch.setattr(country_api_repository, '_send_request', return_mock)

    yield country_api_repository


@pytest_asyncio.fixture
async def country_api_response() -> list:
    return [
        {
            'name': {
                'common': 'Russia',
                'official': 'Russian Federation',
                'native_name': {
                    'rus': {
                        'official': 'Российская Федерация',
                        'common': 'Россия'
                    }
                }
            },
            'cca2': 'RU',
            'ccn3': '643',
            'cca3': 'RUS',
            'cioc': 'RUS',
            'independent': True,
            'status': 'officially-assigned',
            'currencies': {
                'RUB': {
                    'name': 'Russian ruble',
                    'symbol': '₽'
                },
            },
            'capital': ['Москва'],
            'region': 'Europe',
            'subregion': 'Eastern Europe',
            'languages': {'rus': 'Russian', 'eng': 'English'},
            'translations': {
                'rus': {
                    'official': 'Российская Федерация',
                    'common': 'Россия'
                },
            },
            'area': 17098242.0,
            'population': 144104080,
            'capitalInfo': {
                'latlng': [55.75, 37.6]
            },
        }
    ]


@pytest_asyncio.fixture
async def patched_geocoder_api_repository_for_country(
    monkeypatch: MonkeyPatch,
    geocoder_api_country_response: dict
):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param geocoder_api_country_response: expected country response from geocoder API

    :return: patched GeocoderAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(geocoder_api_country_response), HTTPStatus.OK)

    geocoder_api_repository = GeocoderAPIRepository()
    monkeypatch.setattr(geocoder_api_repository, '_send_request', return_mock)

    yield geocoder_api_repository


@pytest_asyncio.fixture
async def geocoder_api_country_response() -> dict:
    return {
        'response': {
            'GeoObjectCollection': {
                'metaDataProperty': {
                    'GeocoderResponseMetaData': {
                        'request': 'Росия',
                        'results': '1',
                        'suggest': 'Ро<fix>сс</fix>ия',
                        'found': '1'
                    }
                },
                'featureMember': [
                    {
                        'GeoObject': {
                            'metaDataProperty': {
                                'GeocoderMetaData': {
                                    'precision': 'other',
                                    'text': 'Россия',
                                    'kind': 'country',
                                    'Address': {
                                        'country_code': 'RU',
                                        'formatted': 'Россия',
                                        'Components': [
                                            {'kind': 'country',
                                             'name': 'Россия'}
                                        ]
                                    },
                                    'AddressDetails': {
                                        'Country': {'AddressLine': 'Россия',
                                                    'CountryNameCode': 'RU',
                                                    'CountryName': 'Россия'}
                                    }
                                }
                            },
                            'name': 'Россия',
                            'boundedBy': {
                                'Envelope': {'lowerCorner': '19.484764 41.185996',
                                             'upperCorner': '191.128012 81.886117'}
                            },
                            'Point': {
                                'pos': '99.505405 61.698657'
                            }}}]}}}


@pytest_asyncio.fixture
async def expected_geocoder_country_result() -> GeocoderSchema:
    return GeocoderSchema(
        name='Россия',
        full_address='Россия',
        coordinates='99.505405 61.698657',
        country_code='RU',
        search_type='country',
    )


@pytest_asyncio.fixture
async def patched_geocoder_api_repository_for_city(
    monkeypatch: MonkeyPatch,
    geocoder_api_city_response: dict
):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param geocoder_api_city_response: expected city response from geocoder API

    :return: patched GeocoderAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(geocoder_api_city_response), HTTPStatus.OK)

    geocoder_api_repository = GeocoderAPIRepository()
    monkeypatch.setattr(geocoder_api_repository, '_send_request', return_mock)

    yield geocoder_api_repository


@pytest_asyncio.fixture
async def geocoder_api_city_response() -> dict:
    return {
        'response': {
            'GeoObjectCollection': {
                'metaDataProperty': {
                    'GeocoderResponseMetaData': {
                        'request': 'Гурьевск',
                        'results': '10',
                        'found': '2'
                    }
                },
                'featureMember': [
                    {
                        'GeoObject': {
                            'metaDataProperty': {
                                'GeocoderMetaData': {
                                    'precision': 'other',
                                    'text': 'Россия, Калининградская область, Гурьевск',
                                    'kind': 'locality',
                                    'Address': {
                                        'country_code': 'RU',
                                        'formatted': 'Россия, Калининградская область, Гурьевск',
                                        'Components': [
                                            {
                                                'kind': 'country',
                                                'name': 'Россия'
                                            },
                                            {
                                                'kind': 'province',
                                                'name': 'Северо-Западный федеральный округ'
                                            },
                                            {
                                                'kind': 'province',
                                                'name': 'Калининградская область'
                                            },
                                            {
                                                'kind': 'area',
                                                'name': 'Гурьевский муниципальный округ'
                                            },
                                            {
                                                'kind': 'locality',
                                                'name': 'Гурьевск'
                                            }
                                        ]
                                    },
                                    'AddressDetails': {
                                        'Country': {
                                            'AddressLine': 'Россия, Калининградская область, Гурьевск',
                                            'CountryNameCode': 'RU',
                                            'CountryName': 'Россия',
                                            'AdministrativeArea': {
                                                'AdministrativeAreaName': 'Калининградская область',
                                                'SubAdministrativeArea': {
                                                    'SubAdministrativeAreaName': 'Гурьевский муниципальный округ',
                                                    'Locality': {
                                                        'LocalityName': 'Гурьевск'
                                                    }}}}}}
                            },
                            'name': 'Гурьевск',
                            'description': 'Калининградская область, Россия',
                            'boundedBy': {
                                'Envelope': {
                                    'lowerCorner': '20.56515 54.754724',
                                    'upperCorner': '20.666623 54.798146'
                                }
                            },
                            'Point': {
                                'pos': '20.608359 54.770401'
                            }
                        }
                    },
                    {
                        'GeoObject': {
                            'metaDataProperty': {
                                'GeocoderMetaData': {
                                    'precision': 'other',
                                    'text': 'Россия, Кемеровская область, Гурьевск',
                                    'kind': 'locality',
                                    'Address': {
                                        'country_code': 'RU',
                                        'formatted': 'Россия, Кемеровская область, Гурьевск',
                                        'Components': [
                                            {
                                                'kind': 'country',
                                                'name': 'Россия'
                                            },
                                            {
                                                'kind': 'province',
                                                'name': 'Сибирский федеральный округ'
                                            },
                                            {
                                                'kind': 'province',
                                                'name': 'Кемеровская область'
                                            },
                                            {
                                                'kind': 'area',
                                                'name': 'Гурьевский муниципальный округ'
                                            },
                                            {
                                                'kind': 'locality',
                                                'name': 'Гурьевск'
                                            }
                                        ]
                                    },
                                    'AddressDetails': {
                                        'Country': {
                                            'AddressLine': 'Россия, Кемеровская область, Гурьевск',
                                            'CountryNameCode': 'RU',
                                            'CountryName': 'Россия',
                                            'AdministrativeArea': {
                                                'AdministrativeAreaName': 'Кемеровская область',
                                                'SubAdministrativeArea': {
                                                    'SubAdministrativeAreaName': 'Гурьевский муниципальный округ',
                                                    'Locality': {
                                                        'LocalityName': 'Гурьевск'
                                                    }}}}}}
                            },
                            'name': 'Гурьевск',
                            'description': 'Кемеровская область, Россия',
                            'boundedBy': {
                                'Envelope': {
                                    'lowerCorner': '85.861523 54.227254',
                                    'upperCorner': '86.015261 54.313682'
                                }
                            },
                            'Point': {
                                'pos': '85.947635 54.285935'
                            }}},
                ]}}
    }


@pytest_asyncio.fixture
async def expected_geocoder_city_result() -> list[GeocoderSchema]:
    return [
        GeocoderSchema(
            name='Гурьевск',
            full_address='Россия, Калининградская область, Гурьевск',
            coordinates='20.608359 54.770401',
            country_code='RU',
            search_type='locality',
        ),
        GeocoderSchema(
            name='Гурьевск',
            full_address='Россия, Кемеровская область, Гурьевск',
            coordinates='85.947635 54.285935',
            country_code='RU',
            search_type='locality',
        ),
    ]


@pytest_asyncio.fixture
async def patched_geocoder_api_repository_not_found(
    monkeypatch: MonkeyPatch,
    geocoder_api_not_found_response: dict
):
    """
    This fixture for override _send_request method

    :param monkeypatch: fixture for monkey-patching
    :param geocoder_api_not_found_response: expected response with no result from geocoder API

    :return: patched GeocoderAPIRepository
    """
    async def return_mock(*args, **kwargs):
        return MockClientResponse(json.dumps(geocoder_api_not_found_response), HTTPStatus.OK)

    geocoder_api_repository = GeocoderAPIRepository()
    monkeypatch.setattr(geocoder_api_repository, '_send_request', return_mock)

    yield geocoder_api_repository


@pytest_asyncio.fixture
async def geocoder_api_not_found_response() -> dict:
    return {
        'response': {
            'GeoObjectCollection': {
                'metaDataProperty': {
                    'GeocoderResponseMetaData': {
                        'request': '1',
                        'results': '10',
                        'found': '0'
                    }
                },
                'featureMember': []
            }
        }
    }
