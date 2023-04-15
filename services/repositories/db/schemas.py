from pydantic import BaseModel


class CurrencyCodesSchema(BaseModel):
    """
    Pydantic schema for CountryDBRepository. Using for getting all currency codes for concrete country.
    """
    currency_codes: list[str]


class LanguageNamesSchema(BaseModel):
    """
    Pydantic schema for CountryDBRepository. Using for getting all language names for concrete country.
    """
    languages: list[str]
