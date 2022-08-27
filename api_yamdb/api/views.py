import random
from urllib import request

import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt import views
from reviews.models import Category, Genre, Comment, Review, Title
from users.models import User
from rest_framework.views import APIView

from .permissions import IsOwnerOrAdmin, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)

# from .serializers import GetTokenSerializer, SignUpSerializer


class SignUpViewSet(viewsets.GenericViewSet):
    """ Обработчик запросов к модели User при регистрации """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def send_mesege(self, username):
        user = User.objects.get(username=username)
        email = user.email
        subject = 'confirmation_code'
        message = f'{username} ваш конфирмайшен код {user.confirmation_code}'
        return send_mail(subject, message, 'admin@admin.ru', [email])

    def create(self, request, *args, **kwargs):
        confirmation_code = random.randint(1, 1000000)
        request.data['confirmation_code'] = confirmation_code
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        username = request.data.get('username')
        email = request.data['email']
        # self.send_mesege(username)
        # return Response(
        #     f'мы отправили вам confirmation_code на email: {email}',
        #     status=status.HTTP_201_CREATED,
        #     headers=headers
        # )
        is_registered = User.objects.filter(username=username, email=email)
        if not is_registered.exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.send_mesege(username)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                f'мы отправили вам confirmation_code на email: {email}',
                status=status.HTTP_201_CREATED
            )
        else:
            self.send_mesege(username)
            response = {
                'error': 'Пользователь уже зарегистрирован в системе!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(views.TokenObtainSlidingView):
    serializer_class = GetTokenSerializer


class UserVievSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = "username"

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserMeVievSet(APIView):
    queryset = User.objects.all()
    # http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
    # lookup_field = "username"


# class SignUpViewSet(CreateModelMixin):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializer
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def send_mesege(self, username):
#         user = User.objects.get(username=username)
#         email = user.email
#         subject = 'confirmation_code'
#         message = f'конфирмайшен код {user.confirmation_code}'
#         return send_mail(subject, message, 'admin@admin.ru', [email])

#     def create(self, request):
#         email = request.data.get('email')
#         username = request.data.get('username')
#         is_registered = User.objects.filter(
#             email=email, username=username)
#         if not is_registered.exists():
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             self.send_code(username)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             self.send_code(username)
#             response = {
#                 'error': 'Пользователь уже зарегистрирован в системе!'
#             }
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list',):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    #permission_classes = AdminOrReadOnly


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Review."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    # def perform_update(self, serializer):
    #     title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    #     # сохранить имя автора, если правит не он
    #     review_id = self.kwargs.get('pk')
    #     author = Review.objects.get(pk=review_id).author
    #     serializer.save(
    #         author=author,
    #         title_id=title.id
    #     )


class CommentViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Comment."""
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)

    # def perform_update(self, serializer):
    #     review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
    #     # сохранить имя автора, если правит не он
    #     comment_id = self.kwargs.get('pk')
    #     author = Comment.objects.get(pk=comment_id).author
    #     serializer.save(
    #         author=author,
    #         review_id=review.id
    #     )
