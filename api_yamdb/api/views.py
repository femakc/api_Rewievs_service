import random

import django_filters
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.permissions import AllowAny

from api.permissions import AdminOrReadOnly
from api.serializers import (CategorySerializer, CustomUserSerializer,
                             GenreSerializer, TitleReadSerializer,
                             TitleWriteSerializer, GetTokenSerializer,
                             SignUpSerializer)
from reviews.models import Category, Genre, Title
from users.models import User
from rest_framework_simplejwt import views
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """ Обработчик запросов к модели CustomUser """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class CategoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='name', lookup_expr='contains')

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


class SignUpViewSet(viewsets.ModelViewSet):
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

    def perform_create(self, serializer):
        print('def create')
        print(self.kwargs)
        print(serializer.validated_data)
        confirmation_code = random.randint(1, 1000000)
        # request.data['confirmation_code'] = confirmation_code
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        print(username, email, confirmation_code)
        # username = self.request.data.get('username')
        # email = self.request.data['email']
        is_registered = User.objects.filter(username=username, email=email)
        if not is_registered.exists():
            print("not nor")
            # serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(confirmation_code=confirmation_code)
            self.send_mesege(username)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(
            #     f'мы отправили вам confirmation_code на email: {email}',
            #     status=status.HTTP_200_OK
            # )
        else:
            self.send_mesege(username)
            response = {
                'error': 'Пользователь уже зарегистрирован в системе!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    # def create(self, request, *args, **kwargs):
    #     # print('def create')
    #     confirmation_code = random.randint(1, 1000000)
    #     request.data['confirmation_code'] = confirmation_code
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # self.perform_create(serializer)
    #     # headers = self.get_success_headers(serializer.data)
    #     username = request.data.get('username')
    #     email = request.data['email']
    #     # self.send_mesege(username)
    #     # return Response(
    #     #     f'мы отправили вам confirmation_code на email: {email}',
    #     #     status=status.HTTP_201_CREATED,
    #     #     headers=headers
    #     # )
    #     is_registered = User.objects.filter(username=username, email=email)
    #     if not is_registered.exists():
    #         serializer = self.serializer_class(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         self.send_mesege(username)
    #         # return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(
    #             f'мы отправили вам confirmation_code на email: {email}',
    #             status=status.HTTP_201_CREATED
    #         )
    #     else:
    #         self.send_mesege(username)
    #         response = {
    #             'error': 'Пользователь уже зарегистрирован в системе!'
    #         }
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(views.TokenObtainSlidingView):
    serializer_class = GetTokenSerializer
