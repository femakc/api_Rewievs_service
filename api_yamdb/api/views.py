import random

import django_filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views

from api.permissions import (AdminOrReadOnly, IsAdminRole, IsAuthorOrReadOnly,
                             IsOwnerPatch)
from api.send_email import send_mesege
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserMeSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class SignUpViewSet(viewsets.ModelViewSet):
    """ Обработчик запросов к модели User при регистрации """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        print('def create')
        print(self.kwargs)
        print(serializer.validated_data)
        confirmation_code = random.randint(1, 1000000)
        serializer.validated_data['confirmation_code'] = confirmation_code
        print(serializer.validated_data)
        serializer.is_valid(raise_exception=True)
        print('валидный serializer')
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        print(username, email, confirmation_code)
        is_registered = User.objects.filter(email=email, username=username)
        if not is_registered.exists():
            print('new user')
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.save(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )
            print("new user")
        else:
            print("пользователь есть")

    def create(self, request, *args, **kwargs):
        print("зашли в create")
        request = request.data.copy()
        print(request)
        serializer = self.get_serializer(data=request)
        serializer.is_valid(raise_exception=True)
        print(kwargs)
        print(request)
        confirmation_code = random.randint(1, 1000000)
        request['confirmation_code'] = confirmation_code
        print(request)
        serializer.is_valid(raise_exception=True)
        print('валидный serializer')
        username = request.get('username')
        email = request.get('email')
        print(username, email, confirmation_code)
        is_registered = User.objects.filter(email=email, username=username)
        if not is_registered.exists():
            print('new user')
            serializer.is_valid(raise_exception=True)
            print(request)
            self.perform_create(serializer)
            print("new user, отправляем письмо")
            send_mesege(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("пользователь есть, отправляем письмо")
            send_mesege(username)
            serializer.is_valid(raise_exception=True)
            print(request)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(views.TokenObtainSlidingView):
    serializer_class = GetTokenSerializer


class UserVievSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminRole,)
    search_fields = ['username']
    lookup_field = "username"


class UserMeViewSet(APIView):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated, IsOwnerPatch)

    def get(self, request):
        # print("get userMe")
        data = UserMeSerializer(request.user, many=False).data
        # print(data)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        # print('PATCH in UserMe')
        # print(request.user.role)
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True)
        if serializer.is_valid(raise_exception=True):
            if request.user.role == 'admin':
                serializer.save()

            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='name',
                                         lookup_expr='contains')

    class Meta:
        model = Category
        fields = ['category']


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug',)
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    permission_classes = (AdminOrReadOnly,)

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
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    # queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    # def perform_create(self, serializer):
    #     title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    #     try:
    #         serializer.save(author=self.request.user, title=title)
    #     except IntegrityError:
    #         raise ValidationError('подписка на самого себя')

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)

    # def perform_destroy(self, instance):
    #     review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
    #     instance

    # def perform_update(self, serializer):
    #     review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
    #     # сохранить имя автора, если правит не он
    #     comment_id = self.kwargs.get('pk')
    #     author = Comment.objects.get(pk=comment_id).author
    #     serializer.save(
    #         author=author,
    #         review_id=review.id
    #     )
