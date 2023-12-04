import csv
from typing import Any

from django.core.management.base import BaseCommand
from pathlib import Path

from reviews.models import (
    Title,
    Category,
    Comment,
    Genre,
    Review,
    GenreTitle,
)
from users.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        CSV_DIR = Path('static', 'data')

        '''Add csvfile User'''
        with open(
            Path(CSV_DIR, 'users.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                user.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile Category'''
        with open(
            Path(CSV_DIR, 'category.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile Genre'''
        with open(
            Path(CSV_DIR, 'genre.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile Title'''
        with open(
            Path(CSV_DIR, "titles.csv"),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(
                        id=row['category']
                    ),
                )
                title.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile GenreTitle'''
        with open(
            Path(CSV_DIR, 'genre_title.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                genre = GenreTitle(
                    id=row['id'],
                    title=Title.objects.get(
                        id=row['title_id']
                    ),
                    genre=Genre.objects.get(
                        id=row['genre_id']
                    ),
                )
                genre.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile Review'''
        with open(
            Path(CSV_DIR, 'review.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                review = Review(
                    id=row['id'],
                    title=Title.objects.get(
                        id=row['title_id']
                    ),
                    text=row['text'],
                    author=User.objects.get(
                        id=row['author']
                    ),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                review.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')

        '''Add csvfile Comment'''
        with open(
            Path(CSV_DIR, 'comments.csv'),
            encoding='utf8'
        ) as file:
            self.stdout.write(f'Начинаем импорт из файла {file.name}')
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                comment = Comment(
                    id=row['id'],
                    review=Review.objects.get(
                        id=row['review_id']
                    ),
                    text=row['text'],
                    author=User.objects.get(
                        id=row['author']
                    ),
                    pub_date=row['pub_date'],
                )
                comment.save()
                count += 1
            self.stdout.write(f'Перемещено данных из файла {count}')
