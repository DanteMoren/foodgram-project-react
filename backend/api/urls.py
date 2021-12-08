from django.urls import include, path
from rest_framework import routers
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import (TokenCreateViewSet, TokenDestroyViewSet, TagViewSet,
                    IngredientViewSet, RecipeViewSet)


router = routers.DefaultRouter()

router.register(
    'users',
    DjoserUserViewSet,
    basename='users'
)

router.register(
    'tags',
    TagViewSet,
    basename='tags'
)

router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)


urlpatterns = [
    # path('recipes/<recipe_id>/shoping_cart', shoping_cart, name='purchase'),
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateViewSet.as_view(), name="login"),
    path('auth/token/logout/', TokenDestroyViewSet.as_view(), name="logout"),
    # path('token/logout', token)
]