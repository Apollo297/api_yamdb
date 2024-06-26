# Generated by Django 3.2 on 2023-12-06 18:40

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'пользователь'), ('moderator', 'модератор'), ('admin', 'админ')], default='user', help_text='Пользователь', max_length=9, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.SlugField(help_text='Имя пользователя', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z'), users.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]
