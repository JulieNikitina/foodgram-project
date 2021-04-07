from django import forms

from .models import Ingredient, Recipe, RecipeIngredient
from .utils import convert_ingredients, get_ingredients


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'recipe_text',
            'time_for_cooking',
            'image'
        )
        widgets = {
            'tags': forms.CheckboxSelectMultiple()}

    def clean(self, *args, **kwargs):
        super().clean()
        self.ingredients = get_ingredients(self.data)
        if not self.ingredients:
            return self.add_error(None, 'Необходимо указать хотя бы один ингредиент для рецепта')
        unique_ingredients = set(self.ingredients)
        if len(unique_ingredients) != len(self.ingredients):
            return self.add_error(None, 'Исключите дублирование ингредиентов')
        for ingredient in self.ingredients:
            if not Ingredient.objects.filter(title=ingredient.title):
                return self.add_error(None, f"Ингредиента \"{ingredient.title}\" нет.")

    def save(self, commit=True):
        self.instance.author = self.request.user
        self.save()

        RecipeIngredient.objects.filter(recipe=self.instance).delete()
        amounts = convert_ingredients(self.ingredients, self.instance)

        for name, amount, _ in self.ingredients:
            ingredient = Ingredient.objects.get(name=name)
            RecipeIngredient.objects.create(
                value=amount,
                recipe=self.instance,
                ingredient=ingredient
            )
            self.instance.ingredients.add(ingredient)
        self.save_m2m()
        return self.instance
