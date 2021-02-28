from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'image', 'recipe_text', 'ingredients', 'category', 'time_for_cooking']






# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
