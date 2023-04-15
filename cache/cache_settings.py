import os

import aioredis
from dotenv import load_dotenv

load_dotenv()


REDIS_URL = os.environ['REDIS_URL']
LIVE_CACHE_SECONDS = os.environ['LIVE_CACHE_SECONDS']
REDIS = aioredis.from_url(REDIS_URL, decode_responses=True)
PREFIX_COUNTRY = 'country_'
PREFIX_CITY = 'city_'
