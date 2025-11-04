from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import OperationalError, ProgrammingError

DEFAULT_USERNAME = "Arjun"
DEFAULT_EMAIL = "arjun@example.com"
DEFAULT_PASSWORD = "Bubbles"


class Command(BaseCommand):
    help = "Ensure the default OPS Suite superuser exists."

    def handle(self, *args, **options):  # type: ignore[override]
        User = get_user_model()
        try:
            exists = User.objects.filter(username=DEFAULT_USERNAME).exists()
        except (OperationalError, ProgrammingError):
            self.stdout.write(self.style.ERROR("Database not ready. Run migrations first."))
            return
        if exists:
            self.stdout.write(self.style.SUCCESS("Superuser already present."))
            return
        User.objects.create_superuser(
            username=DEFAULT_USERNAME,
            email=DEFAULT_EMAIL,
            password=DEFAULT_PASSWORD,
        )
        self.stdout.write(self.style.SUCCESS("Superuser created."))
