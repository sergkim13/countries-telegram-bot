from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from django_layer.settings import (
    DJANGO_ADMIN_EMAIL,
    DJANGO_ADMIN_PASSWORD,
    DJANGO_ADMIN_USERNAME,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = DJANGO_ADMIN_USERNAME
            email = DJANGO_ADMIN_EMAIL
            password = DJANGO_ADMIN_PASSWORD
            print(f'Creating account for {username}')
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
