from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls))
]

