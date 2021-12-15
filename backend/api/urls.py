from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from .views import (TokenCreateView, TokenDestroyView, TagViewSet,
                    IngredientViewSet, RecipeViewSet, UserViewSet)


router = routers.DefaultRouter()

router.register(
    'users',
    UserViewSet,
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
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]
