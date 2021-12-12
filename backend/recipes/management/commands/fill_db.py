import csv
from ...models import Ingredient

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('./data/ingredients.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                    )

        self.stdout.write(self.style.SUCCESS('Successfully'))
