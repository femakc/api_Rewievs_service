import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from api.permissions import AdminOrReadOnly
from api.serializers import CustomUserSerializer, \
    GenreSerializer, CategorySerializer, TitleReadSerializer, \
    TitleWriteSerializer

from reviews.models import Title, Genre, Category
from users.models import CustomUser

# from .permissions import IsOwnerOrAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """ Обработчик запросов к модели CustomUser """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


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

