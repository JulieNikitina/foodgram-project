from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'recipe_text',
            'image'
        )
        widgets = {'tags': forms.CheckboxSelectMultiple()}






# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
