from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError

from recipes.models import (
    Tag,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Follow
)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator])
    email = serializers.EmailField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Follow.objects.filter(
                author=obj.id,
                user=request.user
            ).exists()
        return False

    class Meta:
        fields = (
            'username', 'id', 'email', 'first_name',
            'last_name', 'is_subscribed'
        )
        model = User

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return User.objects.create_user(**validated_data)


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator])
    email = serializers.EmailField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'username', 'id', 'email', 'first_name', 'last_name', 'password')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    image = Base64ImageField(
        read_only=True
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='related_ingredients_with_amount',
        read_only=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_сart = serializers.SerializerMethodField(
        read_only=True
    )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                id=obj.id,
                favorite_this=request.user
            ).exists()
        return False

    def get_is_in_shopping_сart(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                id=obj.id,
                shopping_carts=request.user
            ).exists()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_сart',
            'name', 'image', 'text', 'cooking_time'
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='related_ingredients_with_amount',
        required=True
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_сart = serializers.SerializerMethodField(
        read_only=True
    )

    def create_update_recipe(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('related_ingredients_with_amount')
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient_from_list in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient_from_list['id'])
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient_from_list['amount'],
            )
        return recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                id=obj.id,
                favorite_this=request.user
            ).exists()
        return False

    def get_is_in_shopping_сart(self, obj):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            return Recipe.objects.filter(
                id=obj.id,
                shopping_carts=request.user
            ).exists()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_сart',
            'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        """Validate
        ingredient amount can`t be less then 0
        ingredients are unique
        cooking time can`t be less then 0"""
        ingredients = data['related_ingredients_with_amount']
        if not ingredients:
            raise ValidationError(
                'Необходимо указать хотя бы один ингредиент'
            )
        existing_ingredients = []
        for ingredient in ingredients:
            if ingredient.get('amount') <= 0:
                raise ValidationError(
                    'Количество ингредиентов должно быть больше нуля'
                )
            if (
                    ingredient['id']
            ) not in existing_ingredients:
                instance = ingredient['id']
                existing_ingredients.append(instance)
            else:
                raise ValidationError(
                    'Ингредиенты не должны повторяться'
                )
        if data['cooking_time'] <= 0:
            raise ValidationError(
                'Время готовки должно быть больше нуля'
            )
        tags = data['tags']
        existing_tags = []
        for tag in tags:
            if tag in existing_tags:
                raise ValidationError(
                    'Повторяющиеся теги недопустимы'
                )
            existing_tags.append(tag)
        return data

    def create(self, validated_data):
        validated_data_for_create = {
            'tags': validated_data.pop('tags'),
            'related_ingredients_with_amount':
                validated_data.pop('related_ingredients_with_amount')
        }
        recipe = Recipe.objects.create(**validated_data)
        return self.create_update_recipe(recipe, validated_data_for_create)

    def update(self, recipe, validated_data):
        recipe.ingredients.clear()
        recipe.tags.clear()
        recipe = self.create_update_recipe(recipe, validated_data)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class ShopCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(
        read_only=True
    )

    recipes_count = serializers.SerializerMethodField(
        read_only=True
    )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = Recipe.objects.filter(author=obj)[:int(limit)]
        else:
            recipes = Recipe.objects.filter(author=obj)
        serializer = ShopCartSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.count()

    class Meta:
        model = User
        fields = (
            'username', 'id', 'email', 'first_name',
            'last_name', 'password', 'is_subscribed',
            'recipes', 'recipes_count'
        )
