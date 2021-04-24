from django import forms

from .models import Ingredient, Recipe, RecipeIngredient


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
        self.ingredients = {}
        for key, name in self.data.items():
            if name not in self.ingredients:
                if key.startswith('nameIngredient'):
                    value = key.replace('name', 'value')
                    self.ingredients[name] = self.data[value]
            else:
                self.add_error(
                    None,
                    'Исключите дублирование ингредиентов.'
                )
        if not self.ingredients:
            return self.add_error(
                None,
                'Чтобы сварить кашу, нужен хотя бы топор! Добавь ингредиент.'
            )
        for ingredient in self.ingredients:
            if not Ingredient.objects.filter(title=ingredient):
                return self.add_error(
                    None,
                    f'Ингредиента "{ingredient}" нет.'
                )

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.instance.save()

        RecipeIngredient.objects.filter(recipe=self.instance).delete()

        for name, amount in self.ingredients.items():
            ingredient = Ingredient.objects.get(title=name)
            print(ingredient)
            RecipeIngredient.objects.create(
                quantity=amount,
                recipe=self.instance,
                ingredient=ingredient
            )
            self.instance.ingredients.add(ingredient)
        self.save_m2m()
        return self.instance
