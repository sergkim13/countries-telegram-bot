import asyncio

from django.core.management.base import BaseCommand

from aiogram_layer.src.app import bot, dp


class Command(BaseCommand):
    async def main(self):
        return await dp.start_polling(bot)

    def handle(self, *args, **options):
        asyncio.run(self.main())
