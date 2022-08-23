from rest_framework import serializers

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
