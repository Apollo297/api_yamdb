from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models
from django.utils import timezone

User = get_user_model()


class Common(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=settings.MAX_NAME_LENGTH

    )

    class Meta:
        abstract = True
        ordering = ['-name']


class Category(Common):
    slug = models.SlugField(
        'Код категории',
        unique=True
    )

    class Meta(Common.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(Common):

    slug = models.SlugField(
        'Код жанра',
        unique=True)

    class Meta(Common.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Творение',
        max_length=settings.MAX_NAME_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска творения',
        validators=[
            MaxValueValidator(
                timezone.now().year
            )
        ]
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    description = models.TextField(
        'Описание творения',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'
        ordering = ['-year']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'
            ),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Творение'

    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Творение'
    )
    text = models.TextField(
        'Текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]

    def __str__(self):
        return self.your_field_name[0:settings.MAX_BIG_TEXT_FIELD_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        'Комментарий к отзыву'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.your_field_name[0:settings.MAX_BIG_TEXT_FIELD_LENGTH]
