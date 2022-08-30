import random
from urllib import request
from django.db.models import Avg
import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import IsAuthorOrReadOnly, IsAdminRole
from .send_email import send_mesege
from api.permissions import AdminOrReadOnly

from .serializers import (CategorySerializer, CommentSerializer, 
                        GenreSerializer, GetTokenSerializer, 
                        ReviewSerializer, SignUpSerializer, 
                        TitleReadSerializer, TitleWriteSerializer, 
                        UserMeSerializer, UserSerializer)


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
            # serializer = self.serializer_class(data=serializer.validated_data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.save(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )
            print("new user")
            # send_mesege(username)
            # self.send_code(username)
            # return Response('return после создания', status=status.HTTP_201_CREATED)
        else:
            print("пользователь есть")
            # send_mesege(username)
            # return Response("serializer.data", status=status.HTTP_200_OK) *******************
            # response = {
            #     'error': 'Пользователь уже зарегистрирован в системе!'
            # }
            # return Response(response, status=status.HTTP_400_BAD_REQUEST)


        # serializer.save()
        # username = serializer.validated_data.get('username')
        # send_mesege(username)
        # print(username, email, confirmation_code)
        # return Response("serializer.data", status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print("зашли в create")
        request = request.data.copy()
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(
        #     "create",
        #     status=status.HTTP_201_CREATED,
        #     headers=headers
        # )
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
            # serializer = self.serializer_class(data=serializer.validated_data)
            serializer.is_valid(raise_exception=True)
            print(request)
            self.perform_create(serializer)
            print("new user, отправляем письмо")
            send_mesege(username)
            # self.send_code(username)
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
    permission_classes = (IsAdminRole,)
    # pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = "username"


class UserMeVievSet(APIView):
    # queryset = User.objects.all()
    # http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    # lookup_field = "username"

    # def get(self, request):
    #     user = request.user
    #     user = User.object.filter(username=user.username)

    #     return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        # print(type(user.username))
        # user = User.object.filter(user=user)
        queryset = User.objects.filter(username=user.username)
        # print(queryset)
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = UserSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data, status=status.HTTP_200_OK)

    def patch(self, request):
        print("зашли в PATCH me/")
        user = request.user
        user = User.objects.get(username=user.username)
        
        serializer = UserMeSerializer(user, data=request.data, partial=True)# одно поле не весь объект
        # serializer = self.serializer_class
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Category
        fields = ['category']


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
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
    
    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (Title.objects.prefetch_related('reviews').all().
                        annotate(rating=Avg('reviews__score')).
                        order_by('name'))
            return queryset
        return Title.objects.all()


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,]
    # queryset = Review.objects.all()

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,]

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
