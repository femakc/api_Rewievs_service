from django.db import models
from reviews.validators import validate_year


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Review(models.Model):
    pass


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(default=2000,
                               validators=[validate_year])
    description = models.TextField(default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='categories',
        blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, related_name='genres')
