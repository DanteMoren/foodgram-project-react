import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Load ingredients data to DB'

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=unit,
                )

        self.stdout.write(
            self.style.SUCCESS('Loading of ingredients is successful')
        )

        with open('recipes/data/tags.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, color, slug = row
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug,
                )

        self.stdout.write(self.style.SUCCESS('Loading of tags is successful'))
