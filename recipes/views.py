from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Recipe, Tag, User, Follow, Ingredient, RecipeIngredient, Favorite
from .forms import RecipeForm
from .utils import save_recipe


def index(request):
    recipes = Recipe.objects.order_by('-pub_date').all()
    favorites_list = None
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if not request.user.is_anonymous:
        user = request.user
        favorites_list = (Favorite.objects.filter(user=user).values_list('recipe', flat=True))

    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'favorite_list': favorites_list}
    )


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe.objects.all(), slug=slug)
    return render(request, 'recipe.html', {'recipe': recipe})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view', slug=recipe.slug)

    return render(request, 'recipe_form.html', {'form': form},)


@login_required()
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    url = reverse(
        'recipe_view',
        kwargs={'slug': slug}
    )
    if recipe.author != request.user:
        return redirect(url)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe.amounts.all().delete()
        save_recipe(request, form)
        return redirect(url)
    used_ingredients = recipe.amounts.all()
    edit = True

    return render(
        request,
        'recipe_form.html',
        {
            'form': form,
            'used_ingredients': used_ingredients,
            'edit': edit,
        }
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)
    user = request.user
    following = Follow.objects.filter(
        user=user,
        author=author
    ).exists()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'following': following,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'profile.html', context)


@login_required
def follow_list(request):
    author_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow_list.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def favorite_list(request):
    favorites = Recipe.objects.filter(recipe_favorite__user=request.user)
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    user = request.user
    favorites_list = (Favorite.objects.filter(user=user).values_list('recipe', flat=True))
    return render(
        request,
        'favorite_list.html',
        {'page': page, 'paginator': paginator, 'favorite_list': favorites_list}
    )



def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)

# @login_required
# def add_comment(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         form.instance.author = request.user
#         form.instance.recipe = recipe
#         form.save()
#         return redirect('recipe', recipe_id)
#     return render(request, 'comment.html', {'form': form, 'recipe': recipe})


