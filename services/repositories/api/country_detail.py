import json
from dataclasses import dataclass
from http import HTTPStatus

from aiohttp import ClientConnectorError, ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository
from services.repositories.api.api_schemas import CountrySchema
from services.repositories.api.api_settings import COUNTRY_INFO_URL


@dataclass
class CountryAPIRepository(AbstractAPIRepository):
    """
    This is a class of a RestCountries repository. Provides detailed information about countries
    by sending request to external API "Restcountries.com".
    Extends of the :class:`BaseAPIRepository` class.
    """

    async def get_country_detail(self, country_code: str) -> CountrySchema | None:
        """
        Return details about country by recieved country code.

        :param country_code: country iso code (example: "GB", "CA", "RU")

        :return: country details as :class:`CountrySchema` object or None
        """
        url = f'{COUNTRY_INFO_URL}{country_code}'
        try:
            response = await self._send_request(url=url)
        except ClientConnectorError:
            # may be better raise custom exception
            return None
        if response.status == HTTPStatus.OK:
            return await self._parse_response(response)
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
            resp = await session.get(url=url)
        return resp

    async def _parse_response(self, response: ClientResponse) -> CountrySchema:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response as :class:`CountrySchema` object
        """
        country_data = (json.loads(await response.read()))[0]
        return CountrySchema(
            iso_code=country_data['cca2'],
            name=country_data['translations']['rus']['common'],
            capital=country_data['capital'][0],
            capital_longitude=country_data['capitalInfo']['latlng'][1],
            capital_latitude=country_data['capitalInfo']['latlng'][0],
            area_size=country_data['area'],
            population=country_data['population'],
            currencies={
                currency: country_data['currencies'][currency]['name']
                for currency in country_data['currencies']
            },
            languages=list(
                language for language in country_data['languages'].values()
            )
        )


def get_country_repository() -> CountryAPIRepository:
    """
    Returns object of :class:`CountryAPIRepository` class

    return: :class:`CountryAPIRepository` object
    """
    return CountryAPIRepository()
