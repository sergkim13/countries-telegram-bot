import asyncio
import os
import platform
from typing import Generator

import pytest

pytest_plugins = [
    'services.repositories.api.tests.fixture',
    'services.repositories.db.tests.fixture',
    'aiogram_layer.src.tests.fixtures',
    'cache.test.fixtures',
]

os.environ['WEATHER_API_KEY'] = 'fake_api_key'


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """
        Create event loop for testing
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
