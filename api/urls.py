from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, FavoriteViewSet, IngredientViewSet, PurchaseViewSet

router = DefaultRouter()
router.register('subscriptions', FollowViewSet, basename='follow')
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('purchases', PurchaseViewSet, basename='purchases')


urlpatterns = [
    path('api/', include(router.urls)),
]

