from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RecipeForm
from .models import (Favorite, Follow, Purchase, Recipe, RecipeIngredient, Tag,
                     User)
from .utils import get_tags, save_recipe


def index(request):
    recipes = Recipe.objects.order_by('-pub_date').all()

    tags = get_tags(request)
    all_tags = Tag.objects.all()
    if tags:
        recipes = Recipe.objects.filter(tags__title__in=tags).distinct()

    favorites_list = None
    purchase_list = None
    if not request.user.is_anonymous:
        user = request.user
        favorites_list = (
            Favorite.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )
        purchase_list = (
            Purchase.objects.filter(user=user).values_list(
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
        'purchase_list': purchase_list,
        'tags': tags}

    return render(request, 'index.html', context)


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe.objects.all(), slug=slug)

    favorite_list = None
    purchase_list = None
    following = None

    if not request.user.is_anonymous:
        user = request.user

        following = Follow.objects.filter(
            user=user,
            author=recipe.author.id
        ).exists()

        purchase_list = (
            Purchase.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )

        favorite_list = (
            Favorite.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )

    context = {
        'favorite_list': favorite_list,
        'following': following,
        'purchase_list': purchase_list,
        'recipe': recipe}
    return render(
        request,
        'recipe.html',
        context)


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
    url = reverse('recipe_view', kwargs={'slug': slug})

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


@login_required()
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author == request.user:
        recipe.delete()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)

    favorite_list = None
    purchase_list = None
    following = None

    tags = get_tags(request)
    all_tags = Tag.objects.all()
    if tags:
        recipes = Recipe.objects.filter(
            author=author,
            tags__title__in=tags
        ).distinct()
    if not request.user.is_anonymous:
        user = request.user
        following = Follow.objects.filter(
            user=user,
            author=author
        ).exists()

        purchase_list = (
            Purchase.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )

        favorite_list = (
            Favorite.objects.filter(user=user).values_list(
                'recipe',
                flat=True)
        )

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_tags': all_tags,
        'author': author,
        'favorite_list': favorite_list,
        'following': following,
        'page': page,
        'paginator': paginator,
        'purchase_list': purchase_list,
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

    purchase_list = (
        Purchase.objects.filter(user=user).values_list(
            'recipe',
            flat=True)
    )
    purchase_counter = len(purchase_list)

    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': all_tags,
        'purchase_counter': purchase_counter,
        'purchase_list':  purchase_list,
        'favorite_list': favorites_list,
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'favorite_list.html', context)


def purchase_list(request):
    user = request.user
    cart = Purchase.objects.filter(user=user)
    recipes = Recipe.objects.filter(shopping_list__in=cart)
    purchase_counter = len(recipes)

    context = {
        'purchase_counter': purchase_counter,
        'purchase_list': cart,
        'recipes': recipes,
    }
    return render(request, 'purchase_list.html', context)


@login_required
def download_purchase_list(request):
    recipe_ingredients = (RecipeIngredient.objects
                          .filter(recipe__shopping_list__user=request.user)
                          .select_related('ingredient'))
    purchase_list = {}
    for elem in recipe_ingredients:
        title = elem.ingredient.title
        dimension = elem.ingredient.dimension
        quantity = elem.quantity
        if not purchase_list.get(title):
            purchase_list[title] = [quantity, dimension]
        else:
            purchase_list[title] = [
                purchase_list[title][0] + quantity, dimension
            ]
    if purchase_list:
        file_data = [f'{k.capitalize()}: {v[0]} {v[1]}\n'
                     for k, v in purchase_list.items()]
        response = HttpResponse(
            file_data,
            content_type='application/text charset=utf-8'
        )
        response['Content-Disposition'] = ('attachment; '
                                           'filename="purchase_list.txt"')
        return response
    return redirect('index')


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
