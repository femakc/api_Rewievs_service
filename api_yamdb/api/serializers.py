from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .send_email import send_mesege


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
        # print('singUp validate!!!')
        # print(data)
        # print(data['email'])
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me' "
            )
        user = User.objects.filter(email=data['email'])
        # print(user)
        if user:
            print("User с таким email существует проверяем username")
            username = User.objects.filter(
                username=data['username'],
                email=data['email']
            )
            # print(username)
            if username:
                # print("отправляем письмо")
                send_mesege(data['username'])
            else:
                raise serializers.ValidationError(
                    "user не соответсятвует email"
                )
        else:
            # print("User с таким email НЕ существует проверяем username")
            username = User.objects.filter(username=data['username'])
            # print(username)
            if username:
                raise serializers.ValidationError(
                    "email НЕ соответствуе User "
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
    # print('userMe serializer')

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
        # print(attrs)
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
        # print(user)
        confirm_code = user.confirmation_code
        # print(confirm_code)
        token = self.get_token(user)
        data = OrderedDict()
        data["token"] = str(token)
        if confirmation_code != confirm_code:
            raise exceptions.ValidationError(
                "Confirmation_code не совпадает с тем что в базе"
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


# class ReviewSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Review"""
#     author = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='username'
#     )
#     title = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='title'
#     )

#     class Meta:
#         fields = '__all__'
#         model = Review


# class CommentSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Comment"""
#     author = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='username'
#     )
#     review = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='review'
#     )

#     class Meta:
#         fields = '__all__'
#         model = Comment


# class GenreSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = ('name', 'slug')
#         model = Genre
#         lookup_field = 'slug'


# class CategorySerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = ('name', 'slug')
#         model = Category
#         lookup_field = 'slug'


# class TitleReadSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(many=True)
#     rating = serializers.IntegerField(read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Title


# class TitleWriteSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#         many=True
#     )

    #def validate(self, value):
    #    now = timezone.now().year
    #    if value > now:
    #        raise ValidationError(
    #            f'год выпуска {value} не может быть больше настоящего {now}'
    #         )

    # class Meta:
    #     fields = '__all__'
    #     model = Title