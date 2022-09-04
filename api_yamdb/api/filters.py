import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Обработчик фильтрации произведений."""
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']
