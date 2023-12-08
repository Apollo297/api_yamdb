from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.utils import my_max_length
from users.validators import validate_username


class User(AbstractUser):
    username = models.SlugField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=settings.MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'
            ),
            validate_username
        ],
    )
    email = models.EmailField(
        'Электронная почта',
        help_text='Электронная почта',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=my_max_length(
            settings.USER_ROLES
        ),
        verbose_name='Роль',
        choices=settings.USER_ROLES,
        default=settings.USER,
        help_text='Пользователь',
    )

    class Meta:
        ordering = ('-username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == settings.ADMIN
            or self.is_staff or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    def __str__(self):
        return self.username[:settings.SYMBOL_LIMIT]
