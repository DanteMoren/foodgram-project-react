from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

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
        if str(request.user) != 'AnonymousUser':
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
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.IntegerField()

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

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
        if str(request.user) != 'AnonymousUser':
            return Recipe.objects.filter(
                id=obj.id,
                favorite_this=request.user
            ).exists()
        return False

    def get_is_in_shopping_сart(self, obj):
        request = self.context.get('request')
        if str(request.user) != 'AnonymousUser':
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

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if str(request.user) != 'AnonymousUser':
            return Recipe.objects.filter(
                id=obj.id,
                favorite_this=request.user
            ).exists()
        return False

    def get_is_in_shopping_сart(self, obj):
        request = self.context.get('request')
        if str(request.user) != 'AnonymousUser':
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('related_ingredients_with_amount')
        recipe = Recipe.objects.create(**validated_data)
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

    def update(self, recipe, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('related_ingredients_with_amount')
        recipe.ingredients.clear()
        for ingredient_from_list in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient_from_list['id'])
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient_from_list['amount'],
            )
        tags = validated_data.pop('tags')
        for tag in tags:
            recipe.tags.add(tag)
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
        return len(Recipe.objects.filter(author=obj))

    class Meta:
        model = User
        fields = (
            'username', 'id', 'email', 'first_name',
            'last_name', 'password', 'is_subscribed',
            'recipes', 'recipes_count'
        )
