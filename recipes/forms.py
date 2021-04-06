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
        widgets = {'tags': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, kwargs):
        super().__init__(*args, kwargs)
        self.ingredients = get_ingredients(self.data)

    def clean(self, *args, **kwargs):
        super().clean()
        if not self.ingredients:
            return self.add_error(None, 'Необходимо указать хотя бы один ингредиент для рецепта')
        unique_ingredients = list({(v['title'], v['dimension']): v for v in self.ingredients}.values())
        if len(unique_ingredients) != len(self.ingredients):
            return self.add_error(None, 'Исключите дублирование ингредиентов')
        for ingredient in self.ingredients:
            if not Ingredient.objects.filter(name=ingredient['title'], dimension=ingredient['dimension']):
                return self.add_error(None, f"Ингредиента \"{ingredient['title']}\" нет.")

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.instance.author = self.request.user
        self.instance.save()

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
