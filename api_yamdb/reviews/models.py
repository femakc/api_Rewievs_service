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


# class Review(models.Model):
#     pass


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='titles')
    year = models.IntegerField(default=2000)
    # rating = models.ManyToManyField(Review, related_name='film_rating')
    description = models.TextField(default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='categories',
        blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, related_name='genres')


class Review(models.Model):
    """Отзывы пользователей на контент"""

    SCORE_CHOICES = (
        (1, '1. Очень плохо. Не понравилось совсем.'),
        (2, '2. Плохо. Не понравилось почти всё.'),
        (3, '3. Не очень. Не понравилось многое.'),
        (4, '4. Так себе. Мало что понравилось.'),
        (5, '5. Ни то, ни сё. Почти ничего не понравилось.'),
        (6, '6. Неплохо. Кое-что понравилось.'),
        (7, '7. Хорошо. Многое понравилось.'),
        (8, '8. Очень хорошо. Почти всё понравилось.'),
        (9, '9. Великолепно. Очень понравилось.'),
        (10, '10. Высший балл. В восторге.'),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    def __str__(self):
        # return self.text
        return (f'{self.author.username}, {self.text}, {self.score}')


class Comment(models.Model):
    """Комментарии пользователя на отзыв."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария'
    )

    def __str__(self):
        # return self.text
        return (f'{self.author.username}, {self.text}')