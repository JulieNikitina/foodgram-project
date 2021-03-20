from decimal import Decimal

from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, RecipeIngredient


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            ingredients = get_ingredients(request.POST)
            amounts = convert_ingredients(ingredients, recipe)
            RecipeIngredient.objects.bulk_create(amounts)
            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def get_ingredients(post):
    ingredients = {}
    for key, name in post.items():
        if key.startswith("nameIngredient"):
            value = key.replace("name", "value")
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




