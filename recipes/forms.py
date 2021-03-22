from django import forms

from .models import Recipe


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
