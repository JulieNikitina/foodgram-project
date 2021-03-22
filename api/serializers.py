from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'author')
        model = Follow
        read_only_fields = ['user', 'author']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'recipe')
        model = Favorite
        read_only_fields = ['user', 'recipe']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'recipe')
        model = Purchase
        read_only_fields = ['user', 'recipe']
