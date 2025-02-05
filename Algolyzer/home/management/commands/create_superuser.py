import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if it doesn't exist"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username, email=email, password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Superuser {username} created successfully.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Superuser {username} already exists.")
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "Superuser credentials not provided. Skipping creation."
                )
            )
