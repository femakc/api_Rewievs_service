from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, GetTokenView, UserVievSet, UserMeVievSet

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', SignUpViewSet, basename='signup')
# router.register(r'api/v1/users/me', UserMeVievSet, basename='usersme')
router.register(r'api/v1/users', UserVievSet, basename='users')


urlpatterns = [
    path('api/v1/users/me/', UserMeVievSet, name='userme'),
    path('', include(router.urls)),
    path(
        'api/v1/auth/token/',
        GetTokenView.as_view(),
        name='users'
    ),
]
