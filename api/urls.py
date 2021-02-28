from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, FavoriteViewSet

router = DefaultRouter()
router.register('subscriptions', FollowViewSet, basename='follow')
router.register('favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]

