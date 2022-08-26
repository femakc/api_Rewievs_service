from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('anon', 'Аноним'),
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер Django'),
)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    confirm_code = models.CharField(max_length=6)
    bio = models.TextField('Биография', default='', blank=True, null=True,)
    role = models.CharField(
        'Роль пользователя',
        max_length=32,
        choices=CHOICES,
        default='user'
    )
