from decimal import Decimal

from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, RecipeIngredient


def get_ingredients(post):
    ingredients = {}
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            value = key.replace('name', 'value')
            ingredients[name] = post[value]
    return ingredients


def convert_ingredients(ingredients, recipe):
    elems = []
    for title, quantity in ingredients.items():
        amount = Decimal(quantity.replace(',', '.'))
        ingredient = get_object_or_404(Ingredient, title=title)
        elems.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                quantity=amount)
        )
    return elems


def get_tags(request):
    tags = set()
    if 'tags' in request.GET:
        tags = set(request.GET.getlist('tags'))
    return tags
