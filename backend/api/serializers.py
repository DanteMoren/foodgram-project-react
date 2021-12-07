import datetime as dt

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from users.models import User
from users.validators import username_not_me_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'id', 'email', 'first_name', 'last_name')
        model = User
    # TODO добавить is subscibed в вывод списка пользователей и конкретного пользователя
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# class SignupSerializer(serializers.Serializer):

#     username = serializers.CharField(validators=[
#         UnicodeUsernameValidator, username_not_me_validator])
#     email = serializers.EmailField(required=True, allow_blank=False)

#     class Meta:
#         fields = ('username', 'email')

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# class TokenSerializer(serializers.Serializer):
#     username = serializers.CharField(validators=[
#         UnicodeUsernameValidator, username_not_me_validator])
#     confirmation_code = serializers.CharField()

#     class Meta:
#         fields = ('username', 'confirmation_code')
