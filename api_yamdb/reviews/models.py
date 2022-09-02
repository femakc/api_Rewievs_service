from django.db import models
from .validators import validate_year
from users.models import User
from api_yamdb.settings import SCORE_CHOICES


class Category(models.Model):
    """Категории произведений: «Книги», «Фильмы», «Музыка».
    Список категорий может быть расширен администратором
    """
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Genre(models.Model):
    """Жанр произведения:«Сказка», «Рок» или «Артхаус».
    Новые жанры может Добавлять только администратор.
    """
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


class Title(models.Model):
    """Основное произведение, на который пишется отзыв.
    Наполнение доступно администратору.
    """
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        default=2000,
        validators=[validate_year]
    )
    description = models.TextField(default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='categories',
        blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, related_name='genres1')


class Review(models.Model):
    """Отзывы пользователей на контент.
    Пользователь может оставить лишь один отзыв на произведение.
    Только хозяин отзыва может редактировать отзыв.
    Модератор может менять текст и оценку или удалять полностью объект.
    Администратор - как модератор."""

    # SCORE_CHOICES = (
    #     (1, '1. Очень плохо. Не понравилось совсем.'),
    #     (2, '2. Плохо. Не понравилось почти всё.'),
    #     (3, '3. Не очень. Не понравилось многое.'),
    #     (4, '4. Так себе. Мало что понравилось.'),
    #     (5, '5. Ни то, ни сё. Почти ничего не понравилось.'),
    #     (6, '6. Неплохо. Кое-что понравилось.'),
    #     (7, '7. Хорошо. Многое понравилось.'),
    #     (8, '8. Очень хорошо. Почти всё понравилось.'),
    #     (9, '9. Великолепно. Очень понравилось.'),
    #     (10, '10. Высший балл. В восторге.'),
    # )
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

    def __str__(self):
        return (f'{self.author.username}, {self.text[:30]}')
