<<<<<<< HEAD
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
# from reviews.models import Title, Genre, Category
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериализатор модели CustomUser """
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
=======
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from users.models import User

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from collections import OrderedDict

# from api_yamdb.settings import api_settings
>>>>>>> feature/auth/user


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

<<<<<<< HEAD
class TitleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')



    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category
=======
    # def create(self, validated_data):
    #     return super().create(validated_data)


# class UserMeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'bio',
#             'role'
#         )

>>>>>>> feature/auth/user

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
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='review'
    )

    class Meta:
        fields = '__all__'
        model = Comment