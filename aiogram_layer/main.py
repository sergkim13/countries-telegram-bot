import logging

from aiogram import executor

from aiogram_layer.src.app import dp

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
