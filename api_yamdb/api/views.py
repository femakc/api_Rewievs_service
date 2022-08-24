from rest_framework import permissions, viewsets
from reviews.models import Comment, Review

from api.serializers import CustomUserSerializer, ReviewSerializer, CommentSerializer
from users.models import CustomUser

# from .permissions import IsOwnerOrAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """ Обработчик запросов к модели CustomUser """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Review"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer