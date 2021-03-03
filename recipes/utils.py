from decimal import Decimal

from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, RecipeIngredient


def get_ingredient(request):
    ingredients ={}
    for key, name in request.POST.items():
        if key.startwith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[f'valueIngredient_{num}']
    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            obj = []
            ingredients = get_ingredient(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                obj.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace('.', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(obj)
            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest