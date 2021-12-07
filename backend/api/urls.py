from django.urls import include, path
from rest_framework import routers
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import TokenCreateView, TokenDestroyView

# from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                     ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

v1_router = routers.DefaultRouter()

# v1_router.register(
#     r'categories',
#     CategoryViewSet,
#     basename='categories'
# )
# v1_router.register(
#     r'genres',
#     GenreViewSet,
#     basename='genres'
# )
# v1_router.register(
#     r'titles',
#     TitleViewSet,
#     basename='titles'
# )
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
# )
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )
v1_router.register(
    r'users',
    DjoserUserViewSet,
    basename='users'
)

# v1_router.register(
#     r'users/(?P<user_id>\d+)',
#     UserViewSet,
#     basename='user'
# )

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('auth/token/logout/', TokenDestroyView.as_view(), name="logout"),
    # path('token/logout', token)
]