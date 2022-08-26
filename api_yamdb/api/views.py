import random

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import SignUpSerializer, GetTokenSerializer, UserSerializer
from users.models import CustomUser

from rest_framework_simplejwt import views


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


class UserVievSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели CustomUser."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    # pagination_class = LimitOffsetPagination
