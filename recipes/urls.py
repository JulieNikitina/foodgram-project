from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_recipes, name='category'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('follow/', views.follow_list, name='follow_list'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('users/<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path(
        'users/<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path('users/<str:username>/', views.profile, name='profile'),
]

# path('recipes/<int:recipe_id>/comment/', views.add_comment, name='add_comment'),