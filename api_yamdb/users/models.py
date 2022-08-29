from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

CHOICES = (
    ('anon', 'Аноним'),
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер Django'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    confirmation_code = models.CharField(max_length=32)
    bio = models.TextField('Биография', default='', blank=True, null=True,)
    role = models.CharField(
        'Роль пользователя',
        max_length=32,
        choices=CHOICES,
        default='user'
    )

    def __str__(self):
        return str(self.username)

    # @property
    # def is_staff(self):

    #     # Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


class UserManager(BaseUserManager):
    print('зашли в user manager ')

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
        print('зашли в create_superuser')
        # """
        # Creates and saves a superuser with the given email, date of
        # birth and password.
        # """
        # user = self.create_user(
        #     email,
        #     # username=username,
        #     password=password,
        # )
        # user.is_admin = True
        # user.save(using=self._db)
        # return user
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')  # вот ради этой строчки все и создается

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password=password, **extra_fields)
