from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import User, Follow, Favorite, Ingredient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "user", "author")
        model = Follow
        read_only_fields = ["user", "author"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "user", "recipe")
        model = Favorite
        read_only_fields = ["user", "recipe"]