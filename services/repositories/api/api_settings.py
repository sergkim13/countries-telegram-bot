import os

from dotenv import load_dotenv

load_dotenv()


GEOCODER_URL = os.environ['GEOCODER_URL']
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
YANDEX_API_KEY = os.environ['YANDEX_API_KEY']

COUNTRY_INFO_URL = os.environ['COUNTRY_INFO_URL']
WEATHER_INFO_URL = os.environ['WEATHER_INFO_URL']
CURRENCY_INFO_URL = os.environ['CURRENCY_INFO_URL']

COUNTRY = 'country'
SEARCH_TYPE_LIST = ['province', 'locality']
YANDEX_TAG_LIST = ['<fix>', '</fix>']
