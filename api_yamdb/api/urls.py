from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet, \
    SignUpViewSet, GetTokenView

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', SignUpViewSet, basename='signup')
#router.register(r'api/v1/auth/signup', UserViewSet, basename='users')
router.register('api/v1/titles', TitleViewSet, basename='titles')
router.register('api/v1/categories', CategoryViewSet, basename='categories')
router.register('api/v1/genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'api/v1/auth/token/',
        GetTokenView.as_view(),
        name='users'
    ),
]

