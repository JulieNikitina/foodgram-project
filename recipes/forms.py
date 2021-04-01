from django import forms

from .models import Recipe, RecipeIngredient, Ingredient
from .utils import get_ingredients, convert_ingredients


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
