from django.db import models

from api_yamdb.users.models import CustomUser


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='titles')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    category = models.OneToOneField(
        Category, on_delete=models.PROTECT,
        related_name="posts", blank=True, null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name="posts", blank=True, null=True
    )
