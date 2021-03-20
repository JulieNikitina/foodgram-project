from django.contrib import admin
from .models import Recipe, Tag, Follow, Favorite, Purchase, RecipeIngredient, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'author', 'name', 'image', 'recipe_text', 'time_for_cooking')
    list_filter = ('pub_date', 'author', 'name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
