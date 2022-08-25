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
    
    # email = models.EmailField()
    bio = models.TextField('Биография', default='')
    role = models.CharField(
        'Роль пользователя',
        max_length=32,
        choices=CHOICES,
        default='user'
    )
