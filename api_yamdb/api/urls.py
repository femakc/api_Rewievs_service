from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('api/v1/', include(router.urls))
]

