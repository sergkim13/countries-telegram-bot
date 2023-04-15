from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

warsaw_markup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Польша, Варшава', callback_data='city:21.007139 52.23209')],
                     [InlineKeyboardButton(text='Россия, Алтайский край, Змеиногорский муниципальный район,'
                                                ' муниципальное образование Кузьминский сельсовет, посёлок Варшава',
                                           callback_data='city:81.777584 51.426931')]])
