import csv

from django.core.management.base import BaseCommand
from pathlib import Path

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)
from users.models import User


class Command(BaseCommand):
    help = 'Fills the database with data from csv-file in static folder'

    def handle(self, *args, **kwargs):
        CSV_DIR = Path('static', 'data')
        FILES = (
            (Title, 'titles.csv', {'category': 'category_id'}),
            (Category, 'category.csv', {}),
            (Comment, 'comments.csv', {'author': 'author_id'}),
            (Genre, 'genre.csv', {}),
            (Review, 'review.csv', {'author': 'author_id'}),
            (GenreTitle, 'genre_title.csv', {}),
            (User, 'users.csv', {}),
        )
        for model, file, field_replace in FILES:
            with open(Path(CSV_DIR, file), encoding='utf8') as file:
                self.stdout.write(f'Начинаем импорт из файла {file.name}')
                reader = csv.DictReader(file)
                objects_create = []
                count = 0
                for row in reader:
                    args = dict(**row)
                    count += 1
                    if field_replace:
                        for field_cvs, field_db in field_replace.items():
                            args[field_db] = args.pop(field_cvs)
                model.objects.bulk_create(objects_create.append(model(**args)))
                self.stdout.write(f'Перемещено данных из файла {count}')
