from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ReviewViewSet, CommentViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews/', ReviewViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls))
]

