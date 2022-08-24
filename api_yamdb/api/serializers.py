from rest_framework import serializers

from users.models import CustomUser
from reviews.models import Comment, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review"""
    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment"""
    class Meta:
        fields = '__all__'
        model = Comment