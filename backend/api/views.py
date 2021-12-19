from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from api.pagination import LimitPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from djoser import utils
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.conf import settings
from django.contrib.auth import get_user_model
from django.http import FileResponse

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    Follow
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeReadSerializer,
    ShopCartSerializer,
    UserSubscriptionSerializer
)
from .permissions import OwnerOrAdminOrReadOnly
from .filters import RecipesListFilter, IngredientSearchFilter

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
    pagination_class = LimitPageNumberPagination

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
        queryset = Follow.objects.filter(user=user).values_list('author__id')
        authors = User.objects.filter(id__in=queryset)
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
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [OwnerOrAdminOrReadOnly]
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesListFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer

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
            serializer = ShopCartSerializer(recipe)
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
        ).annotate(amount=Sum('amount'))
        product_list = 'Список покупок: \n'
        for ingredient in ingredients:
            name, unit, amount = ingredient
            product_list += f'{name} '
            product_list += f'({unit})'
            product_list += f' — {amount}\n'
        my_file = open('Product_list.txt', 'w+', encoding='utf-8')
        my_file.write(product_list)
        return FileResponse(my_file)
