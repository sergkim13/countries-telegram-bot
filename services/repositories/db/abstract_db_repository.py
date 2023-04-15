from abc import ABC, abstractmethod


class AbstractDBRepository(ABC):
    """
    Abstract class for all DB repositories
    """

    @abstractmethod
    async def create(self, *args, **kwargs):
        """
        Abstract function for creating new record in database
        """
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        """
        Abstract function for updating record in database
        """
        pass

    @abstractmethod
    async def get_by_pk(self, *args, **kwargs):
        """
        Abstract function for retrieving record from database by pk
        """
        pass

    @abstractmethod
    async def get_by_name(self, *args, **kwargs):
        """
        Abstract function for retrieving record from database by name
        """
        pass
