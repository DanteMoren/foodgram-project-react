from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.conf import settings
from djoser import utils
from recipes.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer

class TokenCreateView(DjoserTokenCreateView):
    
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_201_CREATED
        )


class TokenDestroyView(DjoserTokenDestroyView):
    
    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)
        

class TagView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class IngredientView(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer=RecipeSerializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer=RecipeSerializer):
        serializer.save(author=self.request.user)