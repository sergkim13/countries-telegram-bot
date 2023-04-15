from aiogram_layer.src.constants import INVALID_CHARS


def is_city_name_valid(city_name: str) -> bool:
    """
    Validates city name.

    :param city_name: city name from user's message

    :return: True if  city_name is not empty, start with letter and contain only valid chars, else False
    """
    input_chars = set(city_name)
    if not city_name or city_name[0].isdigit() or any(filter(lambda char: char in INVALID_CHARS, input_chars)):
        return False

    return True


def is_country_name_valid(country_name: str) -> bool:
    """
    Validates country name.

    :param country_name: country name from user's message

    :return: True if  country name is not empty, contain no digits and contain only valid chars, else False
    """
    input_chars = set(country_name)
    if not country_name or any(map(lambda char: char.isdigit(), country_name)) or any(
            filter(lambda char: char in INVALID_CHARS, input_chars)):
        return False

    return True
