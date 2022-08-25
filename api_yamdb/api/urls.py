from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, GetTokenView

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', SignUpViewSet, basename='signupusers')
# router.register(r'api/v1/users', GetTokenView, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'api/v1/users/',
        GetTokenView.as_view(),
        name='users'
    ),
]
