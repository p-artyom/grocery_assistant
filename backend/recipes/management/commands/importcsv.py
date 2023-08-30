import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Выполнить импорт данных из csv файлов'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'static' / 'data'
        with open(file_path / 'tags.csv', encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            for row in reader_object:
                if not Tag.objects.filter(slug=row[2]).exists():
                    Tag.objects.create(
                        name=row[0],
                        color=row[1],
                        slug=row[2],
                    )
            print('Данные тегов загружены в БД!')
        with open(file_path / 'ingredients.csv', encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            for row in reader_object:
                if not Ingredient.objects.filter(name=row[0]).exists():
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
            print('Данные ингредиентов загружены в БД!')
