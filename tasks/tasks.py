import asyncio

from cache.cache_module import Cache
from cache.cache_settings import PREFIX_COUNTRY
from cache.cache_settings import REDIS as redis
from django_layer.celery import app
from services.repositories.api.currency import CurrencyAPIRepository

LIMIT_COUNT = 5

currency_rep = CurrencyAPIRepository()


async def update_currency_cache() -> None:
    """
    Updates the currency data in the cache,
    if the record lifetime is more than 10 seconds.
    """
    currency = await CurrencyAPIRepository().get_all_rate()
    if currency:
        _, key_coordinate_list = await redis.scan(match=f'{PREFIX_COUNTRY}*')
        for key_coordinate in key_coordinate_list:
            if int(await redis.ttl(key_coordinate)) > 10:
                key_coordinate = key_coordinate[8:]
                country_schema = await Cache.get_country(key_coordinate)
                if country_schema:
                    currency_keys_dict = country_schema.currencies.keys()
                    for currency_key in currency_keys_dict:
                        value_rate = currency.all_rate.get(currency_key)
                        if value_rate:
                            country_schema.currencies[currency_key] = value_rate
                            await Cache.create_or_update_country(key_coordinate, country_schema)
        await redis.close()


@app.task()
def run_update_cache() -> None:
    """
    Function starts asynchronous tasks for Celery.
    """
    asyncio.run(update_currency_cache())
