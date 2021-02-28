from django.contrib import admin
from .models import Recipe, Category, User, Follow, Favorite


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'image', 'recipe_text', 'ingredients', 'category', 'time_for_cooking')
    search_fields = ('ingredients',)
    list_filter = ('pub_date', 'author', 'name', 'category')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
