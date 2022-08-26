import random

from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import SignUpSerializer, GetTokenSerializer, UserSerializer
from users.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt import views


class SignUpViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """ Обработчик запросов к модели User при регистрации """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def send_mesege(self, username):
        user = User.objects.get(username=username)
        email = user.email
        subject = 'confirmation_code'
        message = f'конфирмайшен код {user.confirmation_code}'
        return send_mail(subject, message, 'admin@admin.ru', [email])

    def create(self, request, *args, **kwargs):
        confirmation_code = random.randint(1, 1000000)
        request.data['confirmation_code'] = confirmation_code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        username = request.data.get('username')
        email = request.data['email']
        self.send_mesege(username)
        return Response(
            f'мы отправили вам confirmation_code на email: {email}',
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GetTokenView(views.TokenObtainSlidingView):
    serializer_class = GetTokenSerializer


class UserVievSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = "username"

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)