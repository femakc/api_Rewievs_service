import random

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer, GetTokenSerializer
from users.models import CustomUser

from rest_framework_simplejwt import views

from rest_framework import filters, mixins, viewsets
from api.serializers import CustomUserSerializer, TitleSerializer, \
    GenreSerializer, CategorySerializer
from reviews.models import Title, Genre, Category

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from api.serializers import (CommentSerializer, CustomUserSerializer,
                             ReviewSerializer)
from reviews.models import Comment, Review, Title

class SignUpViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """ Обработчик запросов к модели CustomUser при регистрации """
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        confirmation_code = random.randint(1, 1000000)
        request.data['confirm_code'] = confirmation_code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email = request.data['email']
        subject = 'confirmation_code'
        message = f'конфирмайшен код {confirmation_code}'
        send_mail(
            subject,
            message,
            'admin@admin.ru',
            [email],
        )
        print(request.data)
        return Response(
            f'мы отправили вам confirmation_code на email: {email}',
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # def send_masege(request):
    #     email = request.data['email']
    #     subject = 'confirmation_code'
    #     message = f'конфирмайшен код {request.data["confirmation_code"]}'
    #     return send_mail(
    #             subject,
    #             message,
    #             'admin@admin.ru',
    #             [email],
    #         )


class GetTokenView(views.TokenObtainSlidingView):
    serializer_class = GetTokenSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)
>>>>>>> feature/review/comments




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