import datetime as dt

from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User
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


# class SignupSerializer(serializers.Serializer):

#     username = serializers.CharField(validators=[
#         UnicodeUsernameValidator, username_not_me_validator])
#     email = serializers.EmailField(required=True, allow_blank=False)
#     password = serializers.PasswordField(required=True, allow_blank=False)

#     class Meta:
#         fields = ('username', 'email')

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True, allow_blank=False)
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     class Meta:
#         fields = ('password', 'email')
