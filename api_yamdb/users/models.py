from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import (
    ADMIN,
    MODERATOR,
    SYMBOL_LIMIT,
    USER
)


class User(AbstractUser):

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    username = models.SlugField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=150,
        blank=False,
        unique=True,
        validators=(
            [RegexValidator(regex=r'^[\w.@+-]+\Z')]
        ),
    )
    email = models.EmailField(
        'Электронная почта',
        help_text='Электронная почта',
        max_length=254,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        help_text='Имя',
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        help_text='Фамилия',
        verbose_name='Фамилия',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        verbose_name='Роль',
        choices=USER_ROLES,
        default=USER,
        help_text='Пользователь',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:SYMBOL_LIMIT]
