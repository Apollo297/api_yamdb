from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Творение',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска творения'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-year']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
