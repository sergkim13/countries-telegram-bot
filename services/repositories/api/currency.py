import json
from http import HTTPStatus

from aiohttp import ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository
from services.repositories.api.api_schemas import AllRateSchema, CurrencySchema
from services.repositories.api.api_settings import CURRENCY_INFO_URL


class CurrencyAPIRepository(AbstractAPIRepository):
    """
    This class is a repository for making requests in currency API.
    """

    async def get_all_rate(self):
        """
        The function returns the full list of currencies and their values

        :return AllRateSchema or None
        """
        response = await self._send_request(url=CURRENCY_INFO_URL)
        if response.status == HTTPStatus.OK:
            currencies = await self._parse_response(response)
            return AllRateSchema(all_rate={key: value.value for key, value in currencies.items()})
        return None

    async def get_rate(self, char_codes: list[str]) -> list[CurrencySchema] | None:
        """
        The function returns the full list of currencies and their values

        :param char_codes: list of currency codes like ["USD", "EUR"]

        :return: list of CurrencySchema if it exists else None
        """
        response = await self._send_request(url=CURRENCY_INFO_URL)
        if response.status == HTTPStatus.OK:
            currencies = await self._parse_response(response)
            if not currencies:
                return None

            requested_currencies = []  # Todo: use list comprehension if possible.
            for char_code in char_codes:
                currency = currencies.get(char_code)
                requested_currencies.append(currency) if currency else None

            if not requested_currencies:
                return None
            return requested_currencies

        return None

    async def _send_request(self, url: str, params=None, body=None) -> ClientResponse:
        """
        Send GET response

        :param url: API url address
        :param params: optional request's query params
        :param body: optional request's body

        :return: response from API
        """

        async with ClientSession() as session:
            resp = await session.get(url=url, params=params)
        return resp

    async def _parse_response(self, response: ClientResponse) -> dict[str, CurrencySchema] | None:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response
        """

        data_cbr = json.loads(await response.read())
        row_currencies = data_cbr.get('Valute')
        if row_currencies:
            parsed_currencies = {
                currency_code: CurrencySchema.parse_obj(row_currencies[currency_code])
                for currency_code in row_currencies
            }

            return parsed_currencies
        return None
