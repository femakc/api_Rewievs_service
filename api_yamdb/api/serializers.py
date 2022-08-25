from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review, Title, Genre, Category
# from reviews.models import Title, Genre, Category
from users.models import CustomUser

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate, get_user_model

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
        # print(attrs)
        username = attrs.get('username')
        print(username)
        user = CustomUser.objects.filter(username=username)
        print(user)
        confirmation_code = user.get('confirm_code')
        print(confirmation_code)
        
        
        # authenticate_kwargs = {
        #     self.username_field: attrs[self.username_field],
        #     "confirm_code": attrs["confirm_code"],
        # }
        # try:
        #     authenticate_kwargs["request"] = self.context["request"]
        # except KeyError:
        #     pass

        # self.user = authenticate(**authenticate_kwargs)

        # if not api_settings.USER_AUTHENTICATION_RULE(self.user):
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages["no_active_account"],
        #         "no_active_account",
        #     )

        # return {}

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