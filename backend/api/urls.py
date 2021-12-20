from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls)),
]
