from django.db import models

from users.models import CustomUser


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
    year = models.IntegerField(default=2000)
    rating = models.ManyToManyField(Review, related_name='film_rating')
    description = models.TextField(default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='categories',
        blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, related_name='genres')
