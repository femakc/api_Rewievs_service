import random

from .send_email import send_mesege
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated  
from rest_framework.views import APIView

from .serializers import (
    SignUpSerializer, GetTokenSerializer,
    UserSerializer, UserMeSerializer
)
from .permissions import IsAdminRole, IsOwnerPatch
from users.models import User
from rest_framework_simplejwt import views


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
        print("get userMe")
        data = UserMeSerializer(request.user, many=False).data
        print(data)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        print('PATCH in UserMe')
        print(request.user.role)
        serializer = UserMeSerializer(request.user, data=request.data, partial=True) 
        if serializer.is_valid(raise_exception=True):
            if request.user.role == 'admin':
                serializer.save()
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
