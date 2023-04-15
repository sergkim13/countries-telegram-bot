from aiogram_layer.src.keyboards import city_detail, main_menu, to_main_menu
from aiogram_layer.src.messages import (
    CITIES_LIST,
    CITY_INFO,
    CITY_NOT_FOUND,
    START_MESSAGE,
    get_city_info_text,
)
from aiogram_layer.src.states import Form
from aiogram_layer.src.tests.keyboards import warsaw_markup
from services.repositories.api.api_schemas import GeocoderSchema

is_city_name_valid_cases = [
    ('Москва', True), ('Нижний Новгород', True), ('London', True), ('сИвастопл', True), ('Комсомольск-на-Амуре', True),
    ('\'s-Hertogenbosch', True), ('Артемовск13', True), ('', False), ('234city', False), ('Вологда&', False),
    ('^*&', False)
]
is_country_name_valid_cases = [
    ('Россия', True), ('USA', True), ('Доминиканская Республика', True), ('кОзахстн', True), ('Коста-Рика', True),
    ('Кот д\'Ивуар', True), ('Уругвай56', False), ('', False), ('234country', False), ('Италия&', False), ('^*(', False)
]

city_info: GeocoderSchema = GeocoderSchema(
    name='Варшава',
    full_address='Польша, Варшава',
    coordinates='21.007139 52.23209',
    country_code='PL',
    search_type='locality'
)

test_start_page_cases = [
    ('/start', None, None, START_MESSAGE, main_menu),
    ('/help', None, None, START_MESSAGE, main_menu),
]
test_process_city_name_cases = [
    ('Москва', Form.city_search, None, CITY_INFO.format(
        city='Москва', full_address='Россия, Москва', coordinates='37.617698 55.755864'), city_detail),
    ('Варшава', Form.city_search, None, CITIES_LIST, warsaw_markup),
    ('qqw', Form.city_search, None, CITY_NOT_FOUND, to_main_menu),
]

test_choose_city_from_list_cases = [
    ('city:21.007139 52.23209', Form.city_search, {
     city_info.coordinates: city_info}, get_city_info_text(city_info), city_detail),
]
