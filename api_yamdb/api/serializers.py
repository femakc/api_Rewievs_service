import random
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from .send_email import send_mesege
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from collections import OrderedDict


# from api_yamdb.settings import api_settings


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для SignUp """
    # confirmation_code = serializers.SerializerMethodField()
    username = serializers.SlugField(max_length=50, min_length=None, allow_blank=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            # 'confirmation_code',
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email'),
        #         message='Имя пользователя и email уже используются'
        #     )
        # ]
    
    # def get_confirmation_code(self, obj):
    #     confirmation_code = random.randint(1, 1000000)
    #     return confirmation_code

    def validate(self, data):
        print('validate!!!')
        print(data)
        print(data['email'])
        user = User.objects.filter(email=data['email'])
        print(user)
        user_data = User.objects.filter(
            username=data['username'],
            email=data['email']
        )
        if user_data:
            send_mesege(data['username'])
            raise serializers.ValidationError(
                "Пользователь с таким email "
                "сцуществует и ему отправленно письмо с "
            )
        if user:
            raise serializers.ValidationError(
                "Пользователь с таким email сцуществует"
            )
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me' "
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """ Сериализаторор для модели User."""
    # username = serializers.SlugField(max_length=50, min_length=None, allow_blank=False)
    # email = serializers.EmailField()

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
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email'),
        #         message='Имя пользователя или email уже используются'
        #     )
        # ]

    def validate(self, data):
        print('validate!!!')
        print(data)
        print(data['email'])
        # user = User.objects.filter(email=data['email'])
        # print(user)
        user = User.objects.filter(username=data['username'])
        user_email = User.objects.filter(email=data['email'])
        print(user_email)
        if user:
            print("username не валидный")
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует "
            )
        if user_email:
            print("email не валидный")
            raise serializers.ValidationError(
                "Пользователь с таким email сцуществует"
            )
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me' "
            )
        return data

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
