from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.views.generic.base import View
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.serializers import FollowSerializer, FavoriteSerializer, IngredientSerializer
from recipes.models import User, Follow, Favorite, Recipe, Ingredient


class MixinSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass


class FollowViewSet(MixinSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        author_id = self.request.data['id']
        serializer.save(user=self.request.user, author=User.objects.get(id=author_id))

    def destroy(self, request, *args, **kwargs):
        author_id = kwargs['pk']
        follow = get_object_or_404(Follow, user=self.request.user, author=User.objects.get(id=author_id))
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(MixinSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        serializer.save(user=self.request.user, recipe=Recipe.objects.get(id=recipe_id))

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs['pk']
        favorite = get_object_or_404(Favorite, user=self.request.user, recipe=Recipe.objects.get(id=recipe_id))
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_field = ('title',)





