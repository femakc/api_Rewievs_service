from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SignUpViewSet, TitleViewSet,
                    UserVievSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', SignUpViewSet, basename='signup')
router.register(r'api/v1/users', UserVievSet, basename='users')
router.register('api/v1/titles', TitleViewSet, basename='titles')
router.register('api/v1/categories', CategoryViewSet, basename='categories')
router.register('api/v1/genres', GenreViewSet, basename='genres')
router.register(
    r'api/v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'api/v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'api/v1/auth/token/',
        GetTokenView.as_view(),
        name='users'
    ),
]
