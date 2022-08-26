from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate, get_user_model


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор модели CustomUser """

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'confirm_code',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
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
        "no_active_account": ("No active account found with the given credentials")
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
        user = CustomUser.objects.get(username=username)
        print(user)
        confirm_code = user.confirm_code
        print(confirm_code)
        
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # if not api_settings.USER_AUTHENTICATION_RULE(self.user):
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages["no_active_account"],
        #         "no_active_account",
        #     )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
