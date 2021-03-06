from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow
from users.serializers import CustomUserSerializer
from api.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def create_update_recipe(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient_from_list in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient_from_list['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient_from_list['amount'],
            )
        return recipe

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )
        read_only_fields = ('author', 'tags',)

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favorites__user=user,
            id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            shopping_cart__user=user,
            id=obj.id
        ).exists()

    def validate(self, data):
        tags = self.initial_data.get('tags')
        if not tags:
            raise ValidationError(
                "???????????????????? ???????????????? ??????"
            )
        if len(tags) != len(set(tags)):
            raise ValidationError("???????? ???????????? ???????? ??????????????????????")
        data["tags"] = tags

        ingredients = self.initial_data.get("ingredients")
        if not ingredients or len(ingredients) < 1:
            raise ValidationError(
                "???? ???????????????? ????????????????????!"
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_item["id"]
            )
            if ingredient in ingredient_list:
                raise ValidationError(
                    "?????????????????????? ???????????? ???????? ??????????????????????!"
                )
            ingredient_list.append(ingredient)

            amount = int(ingredient_item["amount"])
            if amount <= 0 or amount > 32767:
                raise ValidationError(
                    "?????????????? ???????????????? ???? 0 ???? 32767"
                )
        data["ingredients"] = ingredients

        cooking_time = self.initial_data.get("cooking_time")
        if int(cooking_time) <= 0 or int(cooking_time) > 600:
            raise ValidationError(
                "?????????????? ?????????? ?????????????????????????? ???? 0 ???? 600 ??????????"
            )
        data["cooking_time"] = cooking_time
        return data

    def create(self, validated_data):
        validated_data_for_create = {
            'tags': validated_data.pop('tags'),
            'ingredients':
                validated_data.pop('ingredients')
        }
        recipe = Recipe.objects.create(**validated_data)
        return self.create_update_recipe(recipe, validated_data_for_create)

    def update(self, recipe, validated_data):
        recipe.ingredients.clear()
        recipe.tags.clear()
        recipe = self.create_update_recipe(recipe, validated_data)
        return super().update(recipe, validated_data)


class AddRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')
        write_only_fields = ('user', 'recipe')

    def validate(self, data):
        if Favorite.objects.filter(
            user=data['user'],
            recipe=data['recipe']
        ).exists():
            raise ValidationError('???????????? ?????? ???????? ?? ??????????????????!')
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id'
    )
    name = serializers.ReadOnlyField(
        source='recipe.name'
    )
    image = Base64ImageField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time'
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id', 'name', 'image',
            'cooking_time', 'user', 'recipe'
        )
        write_only_fields = ('user', 'recipe')

    def validate(self, data):
        if ShoppingCart.objects.filter(
            user=data['user'],
            recipe=data['recipe']
        ).exists():
            raise ValidationError(
                '???????????? ?????? ???????? ?? ????????????'
                ' ??????????????!'
            )
        return data


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='author.id'
    )
    email = serializers.ReadOnlyField(
        source='author.email'
    )
    username = serializers.ReadOnlyField(
        source='author.username'
    )
    first_name = serializers.ReadOnlyField(
        source='author.first_name'
    )
    last_name = serializers.ReadOnlyField(
        source='author.last_name'
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return AddRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
