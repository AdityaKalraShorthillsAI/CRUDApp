from typing import Any
from django.core.management import BaseCommand
from faker import Faker


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        faker = Faker()
        print(faker.text(max_nb_chars=50))
        print("-"*100)
        print(faker.text(max_nb_chars=1000))