from django.db import models

from users.models import User
from api_yamdb.settings import SCORE_CHOICES
from .validators import validate_year


class Category(models.Model):
    """Категории произведений: «Книги», «Фильмы», «Музыка».
    Список категорий может быть расширен администратором
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='slug категории')
    description = models.TextField(verbose_name='Описание категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    """Жанр произведения:«Сказка», «Рок» или «Артхаус».
    Новые жанры может Добавлять только администратор.
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='slug жанра')
    description = models.TextField(verbose_name='Описание жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name},'


class Title(models.Model):
    """Основное произведение, на который пишется отзыв.
    Наполнение доступно администратору.
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(
        default=2000,
        validators=[validate_year],
        verbose_name='Год выхода произведения'
    )
    description = models.TextField(default='',
                                   verbose_name='Описание произведения')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, verbose_name='Категория произведения'
    )
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Жанр произведения')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы пользователей на контент.
    Пользователь может оставить лишь один отзыв на произведение.
    Только хозяин отзыва может редактировать отзыв.
    Модератор может менять текст и оценку или удалять полностью объект.
    Администратор - как модератор."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва')
    score = models.IntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_one_review'
            ),
        )

    def __str__(self):
        return (
            f'{self.author.username}, {self.text[:30]}, {self.score}'
        )


class Comment(models.Model):
    """Комментарии пользователя на отзыв.
    Только хозяин коммента может редактировать коммент.
    Модератор может менять текст или удалять полностью объект.
    Администратор - как модератор."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария'
    )

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'

    def __str__(self):
        return (f'{self.author.username}, {self.text[:30]}')
