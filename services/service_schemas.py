from pydantic import BaseModel

from django_layer.countries_app.models import Country
from services.repositories.api.api_schemas import CountrySchema
from services.repositories.db.schemas import CurrencyCodesSchema, LanguageNamesSchema


class CityCoordinatesSchema(BaseModel):
    name: str
    longitude: float
    latitude: float


class CountryUOWSchema(BaseModel):
    detail: CountrySchema | Country
    languages: LanguageNamesSchema
    currencies: CurrencyCodesSchema
    capital: CityCoordinatesSchema

    class Config:
        arbitrary_types_allowed = True
