from django.urls import include, path
from rest_framework import routers
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import (TokenCreateView, TokenDestroyView, TagView,
                    IngredientView, RecipeView)

# from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                     ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

router = routers.DefaultRouter()

router.register(
    'users',
    DjoserUserViewSet,
    basename='users'
)

router.register(
    'tags',
    TagView,
    basename='tags'
)

router.register(
    'ingredients',
    IngredientView,
    basename='ingredients'
)

router.register(
    'recipes',
    RecipeView,
    basename='recipes'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('auth/token/logout/', TokenDestroyView.as_view(), name="logout"),
    # path('token/logout', token)
]