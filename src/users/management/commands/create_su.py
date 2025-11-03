from django.core.management import BaseCommand

from users.models import User

import os
from dotenv import load_dotenv

load_dotenv(override=True)



class Command(BaseCommand):
    """Создаем команду для создания суперюзера"""

    def handle(self, *args, **options):

        user = User.objects.create(email= os.getenv("EMAIL_SUPERUSER"))
        user.set_password(os.getenv("PASSWORD_SUPERUSER"))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
