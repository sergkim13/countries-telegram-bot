from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_layer.src.settings import TG_API_TOKEN

bot = Bot(token=TG_API_TOKEN, parse_mode='Markdown')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
