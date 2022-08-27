import random
from urllib import request

from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.generics import CreateAPIView, UpdateAPIView

from .serializers import SignUpSerializer, GetTokenSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin
from users.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt import views


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


class UserMeVievSet(UpdateAPIView):
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
