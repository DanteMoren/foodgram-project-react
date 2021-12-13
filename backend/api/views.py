from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.pagination import LimitOffsetPagination
from djoser.conf import settings
from djoser import utils
from django.contrib.auth import get_user_model
from django.http import FileResponse
from recipes.models import Tag, Ingredient, Recipe, IngredientRecipe, Follow
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShopCartSerializer,
    UserSubscriptionSerializer
    )
from .permissions import OwnerOrAdminOrReadOnly
from .filters import TagsFilter

User = get_user_model()


class TokenCreateView(DjoserTokenCreateView):

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class TokenDestroyView(DjoserTokenDestroyView):

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(DjoserUserViewSet):
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'put', 'patch', 'delete'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=None,
        )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)
        return None

    @action(
        methods=['get'],
        detail=False,
        serializer_class=UserSubscriptionSerializer,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        queryset = Follow.objects.filter(user=user).values_list('author')
        authors = User.objects.none()
        for author_id in queryset:
            author = User.objects.filter(id=author_id[0])
            authors |= author
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/subscribe',
        url_name='subscribe',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        author = generics.get_object_or_404(User, id=kwargs['id'])
        subscription = Follow.objects.filter(
            user=user,
            author=author
        )
        if (
            request.method == 'GET'
            and not subscription.exists()
            and user != author
        ):
            Follow.objects.create(
                user=user,
                author=author
            )
            author = generics.get_object_or_404(User, id=kwargs['id'])
            serializer = UserSubscriptionSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'DELETE' and not subscription.exists():
            return Response(
                {'detail': 'Страница не найдена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif (
            request.method == 'GET'
            and not subscription.exists()
            and user == author
        ):
            return Response(
                {'detail': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'detail': 'Действие уже выполнено'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    
    def get_queryset(self):
        request = self.request
        name = request.GET.get('name')
        print(name)
        queryset = Ingredient.objects.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [OwnerOrAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagsFilter

    def get_queryset(self):
        request = self.request
        recipes = Recipe.objects.all()
        if str(request.user) != 'AnonymousUser':

            is_favorited = request.GET.get('is_favorited')
            if is_favorited is not None:
                if is_favorited == '1':
                    recipes = recipes.filter(favorite_this=request.user)
                else:
                    recipes = recipes.exclude(favorite_this=request.user)

            is_in_shopping_сart = request.GET.get('is_in_shopping_сart')
            if is_in_shopping_сart is not None:
                if is_in_shopping_сart == '1':
                    recipes = recipes.filter(shopping_carts=request.user)
                else:
                    recipes = recipes.exclude(shopping_carts=request.user)

            author_id = request.GET.get('author')
            if author_id:
                recipes = recipes.filter(author__id=author_id)

        return recipes

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
            shopping_carts=user,
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
            favorite_this=user,
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
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_carts=user
            ).values(
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
            except KeyError:
                shop_list[name] = {}
                shop_list[name]['amount'] = amount
                shop_list[name]['measure_unit'] = unit
        product_list = 'Список покупок: \n'
        for name in shop_list:
            product_list += f'{name} '
            product_list += f'({shop_list[name]["measure_unit"]})'
            product_list += f' — {shop_list[name]["amount"]}\n'
        my_file = open('Product_list.txt', 'w+', encoding='utf-8')
        my_file.write(product_list)
        return FileResponse(my_file)
