from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CategoryViewSet, TitleViewSet, GenreViewSet, SignUpViewSet, GetTokenView, CommentViewSet, ReviewViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'api/v1/auth/signup',
    UserViewSet,
    basename='users'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/users/',
        GetTokenView.as_view(),
        name='users'
    ),
]
