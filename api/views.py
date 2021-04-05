from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import (FavoriteSerializer, FollowSerializer,
                             IngredientSerializer, PurchaseSerializer)
from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User


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
        serializer.save(
            user=self.request.user,
            author=User.objects.get(id=author_id)
        )

    def destroy(self, request, *args, **kwargs):
        author_id = kwargs['pk']
        follow = Follow.objects.get(
            user=self.request.user,
            author__id=author_id
        )
        follow.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class FavoriteViewSet(MixinSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        serializer.save(
            user=self.request.user,
            recipe=Recipe.objects.get(id=recipe_id)
        )

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs['pk']
        favorite = get_object_or_404(
            Favorite,
            user=self.request.user,
            recipe=Recipe.objects.get(id=recipe_id)
        )
        favorite.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^title',)


class PurchaseViewSet(MixinSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        serializer.save(
            user=self.request.user,
            recipe=Recipe.objects.get(id=recipe_id)
        )

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs['pk']
        purchase = get_object_or_404(
            Purchase,
            user=self.request.user,
            recipe=Recipe.objects.get(id=recipe_id)
        )
        purchase.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)
