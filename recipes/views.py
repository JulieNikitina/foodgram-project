from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Recipe, Tag, User, Follow, Ingredient, RecipeIngredient, Favorite
from .forms import RecipeForm
from .utils import save_recipe, get_tags


def index(request):
    recipes = Recipe.objects.order_by('-pub_date').all()

    tags = get_tags(request)
    all_tags = Tag.objects.all()
    if tags:
        recipes = Recipe.objects.filter(tags__title__in=tags).distinct()

    favorites_list = None
    if not request.user.is_anonymous:
        user = request.user
        favorites_list = (
            Favorite.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': all_tags,
        'favorite_list': favorites_list,
        'page': page,
        'paginator': paginator,
        'tags': tags}

    return render(request, 'index.html', context)


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
    url = reverse('recipe_view',kwargs={'slug': slug})

    if recipe.author != request.user:
        return redirect(url)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        recipe.amounts.all().delete()
        save_recipe(request, form)
        return redirect(url)
    used_ingredients = recipe.amounts.all()
    edit = True
    context = {
            'edit': edit,
            'form': form,
            'used_ingredients': used_ingredients,
        }
    return render(request, 'recipe_form.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)

    tags = get_tags(request)
    all_tags = Tag.objects.all()
    if tags:
        recipes = Recipe.objects.filter(
            author=author,
            tags__title__in=tags
        ).distinct()

    user = request.user
    following = Follow.objects.filter(
        user=user,
        author=author
    ).exists()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_tags': all_tags,
        'author': author,
        'following': following,
        'page': page,
        'paginator': paginator,
        'tags': tags,
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

    tags = get_tags(request)
    all_tags = Tag.objects.all()
    if tags:
        favorites = Recipe.objects.filter(
            recipe_favorite__user=request.user,
            tags__title__in=tags
        ).distinct()

    user = request.user
    favorites_list = (
        Favorite.objects.filter(user=user).values_list('recipe', flat=True)
    )

    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': all_tags,
        'favorite_list': favorites_list,
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'favorite_list.html', context)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


