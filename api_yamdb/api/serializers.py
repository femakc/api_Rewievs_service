from rest_framework import serializers

from reviews.models import Comment, Review
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser"""
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
