from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from api.serializers import (CommentSerializer, CustomUserSerializer,
                             ReviewSerializer)
from reviews.models import Comment, Review, Title
from users.models import CustomUser

# from .permissions import IsOwnerOrAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """ Обработчик запросов к модели CustomUser """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Review"""
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Comment"""
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)
