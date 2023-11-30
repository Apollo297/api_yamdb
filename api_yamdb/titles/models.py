from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name="slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Катугория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name="slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    year = models.IntegerField(verbose_name="Год выпуска")
    descriptions = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenresTitle",
        related_name="titles",
        verbose_name="Жанр",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return self.name


class GenresTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genretitle",
        verbose_name="Жанр",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="genretitle",
        verbose_name="Произведение",
    )
