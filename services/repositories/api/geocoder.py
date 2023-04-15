import json
from typing import Optional

from aiohttp import ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository
from services.repositories.api.api_schemas import GeocoderSchema
from services.repositories.api.api_settings import (
    COUNTRY,
    GEOCODER_URL,
    SEARCH_TYPE_LIST,
    YANDEX_API_KEY,
    YANDEX_TAG_LIST,
)

for_city = Optional[GeocoderSchema]
for_country = Optional[list[GeocoderSchema]]


class GeocoderAPIRepository(AbstractAPIRepository):

    async def parse_fixed_request_name(self, row_fixed_name: str) -> str:
        """
        The function removes unnecessary tags
        from the city or country name corrected by Yandex.

        :param row_fixed_name: raw string, example with missing letter 'с': 'Рос<fix>с</fix>ия'

        :return: city or country name without tags
        """
        for word in YANDEX_TAG_LIST:
            row_fixed_name = row_fixed_name.replace(word, '')
        return row_fixed_name

    async def get_city(self, city_name: str) -> list[GeocoderSchema] | GeocoderSchema | None:
        """
        Returns basic information about the city,
        if Yandex api confirms that the user entered the city.

        :param city_name: city name

        :return: Latitude and Longitude and country code
        """
        info_city = await self.get_base_info(city_name)
        if isinstance(info_city, list) or info_city and info_city.search_type in SEARCH_TYPE_LIST:
            return info_city
        return None

    async def get_country(self, country_name: str) -> GeocoderSchema | None:
        """
        Returns basic information about the country,
        if Yandex api confirms that the user entered the country.

        :param country_name: country name

        :return: Latitude and Longitude and country code
        """
        info_country = await self.get_base_info(country_name, is_country=True)
        if not isinstance(info_country, list) and info_country and info_country.search_type == COUNTRY:
            return info_country
        return None

    async def get_base_info(self, city_or_country_name: str, is_country=False) -> for_city | for_country:
        """
        Returns country code and city coordinates and type search.

        :param city_or_country_name: country or city name

        :return: Latitude and Longitude and country code
        """
        if is_country:
            url = f'{GEOCODER_URL}{YANDEX_API_KEY}&geocode={city_or_country_name}&results=1'
        else:
            url = f'{GEOCODER_URL}{YANDEX_API_KEY}&geocode={city_or_country_name}'
        response = await self._send_request(url=url)

        return await self._parse_response(response)

    async def _send_request(self, url: str, params=None, body=None) -> ClientResponse:
        """
        Send GET response

        :param url: API url address

        :param params: optional request's query params

        :return: response from API
        """

        async with ClientSession() as session:
            resp = await session.get(url=url, params=params)
        return resp

    async def _parse_response(self, response: ClientResponse) -> for_city | for_country:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parse response
        """
        data_yandex_geocoder = json.loads(await response.read())
        try:
            main_data = data_yandex_geocoder['response']['GeoObjectCollection']
            meta_data = main_data['metaDataProperty']['GeocoderResponseMetaData']
            count_result = int(meta_data['found'])
            right_name = meta_data['request']
            row_fixed_name = meta_data.get('suggest')
        except KeyError:
            return None
        except ValueError:
            return None
        if row_fixed_name:
            right_name = await self.parse_fixed_request_name(row_fixed_name)
        if count_result == 1:
            return await self.parse_one_result(right_name, main_data)
        elif count_result > 1:
            return await self.parse_many_result(right_name, main_data)
        return None

    async def parse_one_result(self, right_name: str, main_data: dict) -> GeocoderSchema | None:
        """
        Function handles one result.

        :param right_name: valid city or country name
        :param main_data: all information about cities or one country

        :return: information about the object or nothing
        """
        try:
            geo_obj = main_data['featureMember'][0]['GeoObject']
            geocoder_meta_data = geo_obj['metaDataProperty']['GeocoderMetaData']
            address_data = geocoder_meta_data['Address']
            coordinates = geo_obj['Point']['pos']
            search_type = geocoder_meta_data['kind']
            full_address = address_data['formatted']
            country_code = address_data['country_code']
        except KeyError:
            return None
        return GeocoderSchema(coordinates=coordinates, country_code=country_code,
                              search_type=search_type, full_address=full_address, name=right_name)

    async def parse_many_result(self, right_name: str, main_data: dict) -> GeocoderSchema | list[GeocoderSchema] | None:
        """
        Function handles many results.

        :param right_name: valid city or country name
        :param main_data: all information about cities or one country

        :return: information about objects or nothing
        """
        geocoder_schema_list = []
        for geo_object in main_data['featureMember']:
            try:
                geo_object = geo_object['GeoObject']
                geo_meta_data = geo_object['metaDataProperty']['GeocoderMetaData']
                address = geo_meta_data['Address']
                search_type = geo_meta_data['kind']
                if search_type in SEARCH_TYPE_LIST:
                    geocoder_schema_list.append(GeocoderSchema(
                        name=right_name,
                        full_address=address['formatted'],
                        coordinates=geo_object['Point']['pos'],
                        search_type=search_type,
                        country_code=address['country_code']
                    )
                    )
            except KeyError:
                pass
        if geocoder_schema_list:
            if len(geocoder_schema_list) > 1:
                return geocoder_schema_list
            return geocoder_schema_list[0]
        return None


# g = GeocoderAPIRepository()
# print(asyncio.run(g.get_city('будапешт')))
