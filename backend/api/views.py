from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets,serializers
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.conf import settings
from djoser import utils
from django.db.models import Value, IntegerField, F
from django.http import FileResponse
from recipes.models import Tag, Ingredient, Recipe, Purchase, IngredientRecipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, ShopCartSerializer

class TokenCreateViewSet(DjoserTokenCreateView):
    
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_201_CREATED
        )


class TokenDestroyViewSet(DjoserTokenDestroyView):
    
    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)
        

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    

    def perform_create(self, serializer=RecipeSerializer):
        serializer.save(author=self.request.user)


    def perform_update(self, serializer=RecipeSerializer):
        serializer.save(author=self.request.user)


    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/shopping_cart',
        url_name='shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        user = request.user
        recipe = generics.get_object_or_404(Recipe, id=kwargs['id'])
        is_added = Recipe.objects.filter(
            shopping_carts = user,
            id=recipe.id
        ).exists()
        if request.method == 'GET' and not is_added:
            recipe.shopping_carts.add(user)
            data = {
            'id': recipe.id,
            'name': recipe.name,
            'image': recipe.image,
            'cooking_time': recipe.cooking_time
            }
            serializer = ShopCartSerializer(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and is_added:
            recipe.shopping_carts.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'DELETE' and not is_added:
            return Response(
            {'detail': 'Страница не найдена.'},
            status=status.HTTP_404_NOT_FOUND
        )
        else:
            return Response(
                {'detail': 'Рецепт уже в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/favorite',
        url_name='favorite',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        user = request.user
        recipe = generics.get_object_or_404(Recipe, id=kwargs['id'])
        like = Recipe.objects.filter(
            favorite_this = user,
            id=recipe.id
        ).exists()
        if request.method == 'GET' and not like:
            recipe.favorite_this.add(user)
            serializer = ShopCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and like:
            recipe.favorite_this.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'DELETE' and not like:
            return Response(
            {'detail': 'Страница не найдена.'},
            status=status.HTTP_404_NOT_FOUND
        )
        else:
            return Response(
                {'detail': 'Действие уже выполнено'},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientRecipe.objects.filter(recipe__shopping_carts=user).values(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount')
        shop_list = {}
        ingredients = ingredients
        for name, unit, amount in ingredients:
            try:
                shop_list[name]['amount'] += amount
            except:
                shop_list[name] = {}
                shop_list[name]['amount'] = amount
                shop_list[name]['measure_unit'] = unit
        product_list = 'Список покупок: \n'
        for name in shop_list:
            product_list += f'{name}'
            product_list += f' {shop_list[name]["amount"]}'
            product_list += f'{shop_list[name]["measure_unit"]}'
            product_list += f' \n'
        my_file = open('Product_list.txt', 'w+', encoding='utf-8')
        my_file.write(product_list)
        return FileResponse(my_file)
