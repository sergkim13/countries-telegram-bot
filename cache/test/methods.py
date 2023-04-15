import json

import pydantic.schema

from cache.cache_settings import REDIS as redis


async def create_test_data(any_key: str, any_data: pydantic.schema) -> None:
    await redis.set(any_key, json.dumps(dict(any_data)))
    await redis.close()


async def clear_redis(any_key: list[str]) -> None:
    await redis.delete(*any_key)
    await redis.close()
