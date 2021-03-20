from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('<slug:slug>/edit', views.recipe_edit, name='recipe_edit'),
    # path('<int:recipe_id>/<slug:slug>/delete', views.recipe_delete, name='recipe_delete'),
    path('<slug:slug>', views.recipe_view, name='recipe_view'),
    path('follow/', views.follow_list, name='follow_list'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('users/<str:username>/', views.profile, name='profile'),
]

# path('recipes/<int:recipe_id>/comment/', views.add_comment, name='add_comment'),