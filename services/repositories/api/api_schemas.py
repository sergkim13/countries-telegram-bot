from pydantic import BaseModel, Field


class AllRateSchema(BaseModel):
    """
    Pydantic schema for CurrencyAPIRepository. Used to get all currencies.
    """

    all_rate: dict


class CurrencySchema(BaseModel):
    """
    Pydantic schema for CurrencyAPIRepository. Using for parsing response from CurrencyAPI.
    """

    id: str = Field(..., alias='ID')
    num_code: str = Field(..., alias='NumCode')
    char_code: str = Field(..., alias='CharCode')
    nominal: int = Field(..., alias='Nominal')
    name: str = Field(..., alias='Name')
    value: float = Field(..., alias='Value')
    previous: float = Field(..., alias='Previous')


class CountrySchema(BaseModel):
    """
    Pydantic schema for CountryAPIRepository. Using for parsing response from CountryAPI.
    """
    iso_code: str
    name: str
    capital: str
    capital_longitude: float
    capital_latitude: float
    area_size: int
    population: int
    currencies: dict[str, str]
    languages: list[str]


class GeocoderSchema(BaseModel):
    """
    Pydantic schema for GeocoderAPIRepository. Using for parsing response from Geocoder API.
    """
    name: str
    full_address: str
    coordinates: str
    country_code: str
    search_type: str


class WeatherSchema(BaseModel):
    temperature: float
    temperature_feels_like: float
    max_temperature: float
    min_temperature: float
    weather_type: str
    humidity: float
    wind_speed: float


class CitySchema(BaseModel):
    name: str
    country_code: str
    longitude: float
    latitude: float
    is_capital: bool
