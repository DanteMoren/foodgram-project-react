from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    CustomUserViewSet,
    TokenCreateView,
    TokenDestroyView
)

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]
