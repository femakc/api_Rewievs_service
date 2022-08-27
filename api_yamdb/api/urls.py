from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SignUpViewSet, TitleViewSet,
                    UserMeVievSet, UserVievSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'api/v1/auth/signup', SignUpViewSet, basename='signupusers')
router.register(r'api/v1/users', UserVievSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
# router.register(
#     r'api/v1/auth/signup',
#     UserViewSet,
#     basename='users'
# )
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
    path('api/v1/users/me/', UserMeVievSet.as_view(), name='userme'),
    path('', include(router.urls)),
    path(
        'api/v1/auth/token/',
        GetTokenView.as_view(),
        name='users'
    ),
]
