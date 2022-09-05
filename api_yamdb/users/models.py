from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from api_yamdb.settings import ROLES_CHOICES


class User(AbstractUser):

    username = models.CharField(
        max_length=100,
        unique=True
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=32,
        verbose_name='код подтверждения',
        help_text='код'
    )
    bio = models.TextField(
        default='',
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Биография пользователя'
    )
    role = models.CharField(
        max_length=32,
        choices=ROLES_CHOICES,
        default='user',
        verbose_name='Роль пользователя',
        help_text='роль'
    )

    def __str__(self):
        return str(self.username)


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('У пользователя должен быть email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password=password, **extra_fields)
