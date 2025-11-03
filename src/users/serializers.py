from typing import Dict, Any

from django.contrib.auth.models import Group
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели User.
        Используется для CRUD операций с пользователями.
        """
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "middle_name", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}, "confirm_password": {"write_only": True}}

    def validate(self, attrs) -> Dict[str, Any]:
        """Проверка совпадения полей"""

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        return attrs

    def create(self, validated_data) -> User:
        """Удаление confirm_password из validated_data"""

        del validated_data["confirm_password"]
        return super().create(validated_data)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели GROUP"""
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]
