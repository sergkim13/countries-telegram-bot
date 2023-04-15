import pytest

from services.repositories.api.api_schemas import CurrencySchema
from services.repositories.api.currency import CurrencyAPIRepository
from services.repositories.api.tests.cases import get_rate_cases


@pytest.mark.asyncio
@pytest.mark.parametrize('char_codes', get_rate_cases)
async def test_get_rate(patched_currency_api_repository: CurrencyAPIRepository, currency_api_response: dict,
                        char_codes: list) -> None:
    """
        Check normal work of get_rate method

    :param patched_currency_api_repository: currency api repository with mocked method _send_request
    :param currency_api_response: normal response from currency API
    """
    currencies = await patched_currency_api_repository.get_rate(char_codes)
    expected_currencies = currency_api_response['Valute']
    expected = [CurrencySchema.parse_obj(expected_currencies.get(char_code))
                for char_code in char_codes if expected_currencies.get(char_code)] or None

    assert currencies == expected, 'Expected list[CurrencySchema] or None'
