from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models

from reviews.validators import validate_year


User = get_user_model()


class NameSlugBaseModel(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=settings.MAX_NAME_LENGTH

    )
    slug = models.SlugField(
        'Слаг',
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('-name',)

    def __str__(self):
        return self.name[:settings.MODEL_NAME_LENGTH]


class TextAuthorPubDateBaseModel(models.Model):
    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.your_field_name[0:settings.MAX_BIG_TEXT_FIELD_LENGTH]


class Category(NameSlugBaseModel):
    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):
    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        'Творение',
        max_length=settings.MAX_NAME_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска творения',
        validators=(
            validate_year,
        )
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
        ordering = ('-year',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'
            ),
        ]

    def __str__(self):
        return self.name[:settings.MODEL_NAME_LENGTH]


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


class Review(TextAuthorPubDateBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Творение'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка',
    )

    class Meta(TextAuthorPubDateBaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(TextAuthorPubDateBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta(TextAuthorPubDateBaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
