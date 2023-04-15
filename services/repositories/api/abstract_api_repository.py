from abc import ABC, abstractmethod

from aiohttp import ClientResponse


class AbstractAPIRepository(ABC):
    """
    Abstract class for all API repositories
    """

    @abstractmethod
    async def _send_request(self, url: str, params=None, body=None) -> ClientResponse:
        """
        Abstract function for sending request
        """
        pass

    @abstractmethod
    async def _parse_response(self, *args, **kwargs):
        """
        Abstract function for parsing response
        """
        pass
