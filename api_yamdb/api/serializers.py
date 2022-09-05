from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .send_email import send_message


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для SignUp """
    username = serializers.SlugField(
        max_length=50,
        min_length=None,
        allow_blank=False
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me' "
            )
        user = User.objects.filter(email=data['email'])
        if user.exists():
            username = User.objects.filter(
                username=data['username'],
                email=data['email']
            )
            if username.exists():
                send_message(data['username'])
            else:
                raise serializers.ValidationError(
                    "user не соответствует email"
                )
        else:
            username = User.objects.filter(username=data['username'])
            if username.exists():
                raise serializers.ValidationError(
                    "email не соответствует User "
                )

        return data


class UserSerializer(serializers.ModelSerializer):
    """ Сериализаторор для модели User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Имя пользователя или email уже используются'
            )
        ]


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class GetTokenSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = AccessToken

    default_error_messages = {
        "no_active_account": (
            "No active account found with the given credentials"
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        is_user = User.objects.filter(
            username=username
        ).exists()
        if not is_user:
            raise exceptions.NotFound(
                "нету такого узера"
            )
        user = User.objects.get(username=username)
        confirm_code = user.confirmation_code
        token = self.get_token(user)
        data = OrderedDict()
        data["token"] = str(token)
        if confirmation_code != confirm_code:
            raise exceptions.ValidationError(
                "Confirmation_code не совпадает с тем что в базе"
            )

        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""

    class Meta:
        exclude = ('id', 'description')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category"""

    class Meta:
        exclude = ('id', 'description')
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method == 'POST'
            and Review.objects.filter(author=user,
                                      title_id=title_id).exists()):
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
