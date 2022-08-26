from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Title, Genre, Category
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериализатор модели CustomUser """
    class Meta:
        model = CustomUser
        fields = '__all__'


# class TitleSerializer(serializers.ModelSerializer):
#
#     def validate(self, value):
#         now = timezone.now().year
#         if value > now:
#             raise ValidationError(
#                 f'год выпуска {value} не может быть больше настоящего {now}'
#             )
#
#     class Meta:
#         fields = '__all__'
#         model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
