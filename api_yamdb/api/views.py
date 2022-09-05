import uuid

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import views

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import GetPostDelMixin
from .permissions import (
    IsAdminRole, IsAuthorOrReadOnly,
    IsOwnerPatch, AdminOrReadOnly
)
from .send_email import send_message
from .serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, GetTokenSerializer,
    ReviewSerializer, SignUpSerializer,
    TitleReadSerializer, TitleWriteSerializer,
    UserMeSerializer, UserSerializer
)


class SignUpViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели User при регистрации."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        confirmation_code = uuid.uuid4()
        serializer.validated_data['confirmation_code'] = confirmation_code
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        is_registered = User.objects.filter(email=email, username=username)
        if not is_registered.exists():
            serializer.save(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )
            send_message(username)
        else:
            send_message(username)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response


class GetTokenView(views.TokenObtainSlidingView):
    """Обработчик получения токенов при регистрации."""
    serializer_class = GetTokenSerializer


class UserVievSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminRole,)
    search_fields = ['username']
    lookup_field = "username"

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsOwnerPatch]
    )
    def me(self, request, pk=None):
        data = UserMeSerializer(request.user, many=False).data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Обработчик самих произведений."""
    queryset = (Title.objects.prefetch_related('reviews').all().
                annotate(rating=Avg('reviews__score')).
                order_by('name'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(GetPostDelMixin):
    """Обработчик жанров произведений."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination


class CategoryViewSet(GetPostDelMixin):
    """Обработчик категории произведений."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик запросов к модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


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
