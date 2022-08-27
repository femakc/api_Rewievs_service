from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
# from reviews.models import Title, Genre, Category
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для SignUp """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'confirmation_code',
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email'),
        #         message='Имя пользователя или email уже используются'
        #     )
        # ]

    # def validate(self, attrs):
    #     return super().validate(attrs)

    # def validate(self, data):
    #     print(data)
    #     user = User.objects.filter(username=data.username, email=data.email)
    #     print(user)
    #     if not user:
    #         raise serializers.ValidationError("Тарам пам пам")

    #     return data


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


# class UserSerializer(serializers.ModelSerializer):
#     """ Сериализаторор для модели Post."""

#     class Meta:
#         model = CustomUser
#         fields = ('__all__')

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
        print(attrs)
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        print(username, confirmation_code)
        user = User.objects.get(username=username)
        print(user)
        confirm_code = user.confirmation_code # надо поправит
        print(confirm_code)
        token = self.get_token(user)
        data = OrderedDict()
        data["token"] = str(token)

        if confirmation_code != confirm_code:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        exclude = ('review',)
        model = Comment


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

    #def validate(self, value):
    #    now = timezone.now().year
    #    if value > now:
    #        raise ValidationError(
    #            f'год выпуска {value} не может быть больше настоящего {now}'
    #         )

    class Meta:
        fields = '__all__'
        model = Title
