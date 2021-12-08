import datetime as dt
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import fields
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from users.models import User
from recipes.models import Tag, Ingredient, IngredientRecipe, Recipe
from users.validators import username_not_me_validator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        UnicodeUsernameValidator, username_not_me_validator])
    email = serializers.EmailField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        fields = (
            'username', 'id', 'email', 'first_name', 'last_name', 'password')
        model = User
    # TODO добавить is subscibed в вывод списка пользователей и конкретного пользователя
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return User.objects.create_user(**validated_data)


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    username = serializers.CharField(validators=[
        UnicodeUsernameValidator, username_not_me_validator])
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
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    # ingredients = IngredientRecipeSerializer(many=True, required=True)
    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
            )
    
    # def create(self, validated_data):
    #     # tags = validated_data['tags']
    #     # ingredients = validated_data['ingredients']
    #     recipe = Recipe.objects.create(**validated_data)
    #     # for tag in tags:
    #     #     recipe.tags.add(tag)
    #     return recipe