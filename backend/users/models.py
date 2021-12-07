from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import username_not_me_validator


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    CHOICES = [(USER, 'user'),
               (ADMIN, 'admin')]

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text=('Никнейм (является необходимым).'
                   '150 символов или меньше.'
                   'Только буквы, цифры и @/./+/-/_.'),
        validators=[username_validator, username_not_me_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует.'),
        },
    )
    first_name = models.CharField(
        'first name',
        max_length=30,
        blank=True,
        null=True,
        help_text=('Имя пользователя')
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True,
        null=True,
        help_text=('Фамилия пользователя')
    )
    email = models.EmailField(
        'Email address',
        blank=False,
        null=False,
        max_length=254,
        unique=True,
        help_text=('Email пользователя'),
        error_messages={
            'unique': ('A user with that email already exists.'),
        })
    role = models.CharField(
        'User role',
        max_length=9,
        choices=CHOICES,
        blank=False,
        default=USER,
        null=False,
        help_text=('Роль пользователя на сайте')
    )

    class Meta:
        ordering = ['-id']
