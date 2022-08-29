import random
from urllib import request

# from django.core.mail import send_mail
from .send_email import send_mesege
from rest_framework import status, viewsets, filters
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView

from .serializers import SignUpSerializer, GetTokenSerializer, UserSerializer, UserMeSerializer
from .permissions import IsOwnerOrAdmin
from users.models import User
from rest_framework.pagination import LimitOffsetPagination
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
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
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

    # def patch(self, request, user_id):
        # user = User.objects.get(id=user_id)
        # serializer = UserSerializer(user, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_400_BAD_REQUEST)


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



        # email = serializer.validated_data.get('email')
        # username = self.request.data.get('username')
        # email = self.request.data['email']
        # is_registered = User.objects.filter(username=username, email=email)
        # if not is_registered.exists():
        #     print("not nor")
        #     # serializer = self.serializer_class(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(confirmation_code=confirmation_code)
        #     send_mesege(username)
        #     # return Response(serializer.data, status=status.HTTP_200_OK)
        #     return Response(
        #         f'мы отправили вам confirmation_code на email: {email}',
        #         status=status.HTTP_200_OK
        #     )
        # else:
        #     print("зарегестрированн !!!!")
        #     send_mesege(username)
        #     response = {
        #         'error': 'Пользователь уже зарегистрирован в системе!'
        #     }
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)



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