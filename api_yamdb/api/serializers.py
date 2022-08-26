from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from users.models import User

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate, get_user_model
from collections import OrderedDict

# from api_yamdb.settings import api_settings


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для SignUp """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'confirm_code',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Имя пользователя или email уже используются'
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """ Сериализаторор для модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


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
        confirm_code = user.confirm_code
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
