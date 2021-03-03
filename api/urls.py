from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, FavoriteViewSet, IngredientViewSet

router = DefaultRouter()
router.register('subscriptions', FollowViewSet, basename='follow')
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]

