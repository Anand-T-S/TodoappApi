from rest_framework.serializers import ModelSerializer
from Todoapi.models import Todos
from django.contrib.auth.models import User
from rest_framework import serializers


class TodoSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Todos
        fields = [
            "id",
            "task_name",
            "user",
            "status"
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        return Todos.objects.create(**validated_data, user=user)  # overrides default create ORM query


class UserSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()