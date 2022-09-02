from django.db import models
from .validators import validate_year
from users.models import User
from api_yamdb.settings import SCORE_CHOICES


class Category(models.Model):
    """Категории произведений: «Книги», «Фильмы», «Музыка».
    Список категорий может быть расширен администратором
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='slug категории')
    description = models.TextField(verbose_name='Описание категории')# удалить это поле

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # добавил verbose_name и verbose_name_plural в Мета классе и в поле


class Genre(models.Model):
    """Жанр произведения:«Сказка», «Рок» или «Артхаус».
    Новые жанры может Добавлять только администратор.
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='slug жанра')
    description = models.TextField(verbose_name='Описание жанра') # удалить это поле

    def __str__(self):
        return f'{self.name},'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        # добавил verbose_name и verbose_name_plural в Мета классе и в поле


class Title(models.Model):
    """Основное произведение, на который пишется отзыв.
    Наполнение доступно администратору.
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(
        default=2000,
        validators=[validate_year],  # добавил валидатор
        verbose_name='Год выхода произведения'
    )
    description = models.TextField(default='',
                                   verbose_name='Описание произведения')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles_category',
        # сменил related_name
        blank=True, null=True, verbose_name='Категория произведения'
    )
    genre = models.ManyToManyField(Genre, related_name='titles_genre',
                                   verbose_name='Жанр произведения')
    # сменил related_name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


        # добавил verbose_name и verbose_name_plural в Мета классе и в поле


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
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']# добавили сортировку
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

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'
