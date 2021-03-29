from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cook.settings import PER_PAGE
from .forms import RecipeForm
from .models import (Favorite, Follow, Purchase, Recipe, RecipeIngredient, Tag,
                     User)
from .utils import get_tags, save_recipe


def index(request):
    tags = get_tags(request)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.by_tags(tags).params_for_query(request.user)

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': all_tags,
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': tags}

    return render(request, 'index.html', context)


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe.objects.params_for_query(request.user), slug=slug)

    context = {'recipe': recipe}
    return render(
        request,
        'recipes/recipe.html',
        context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view', slug=recipe.slug)
    return render(request, 'recipes/recipe_form.html', {'form': form}, )


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
    return render(request, 'recipes/recipe_form.html', context)


@login_required()
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author == request.user:
        recipe.delete()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)

    tags = get_tags(request)
    all_tags = Tag.objects.all()

    recipes = (
        Recipe.objects.by_tags(tags)
        .params_for_query(request.user)
        .filter(author=author)
    )

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_tags': all_tags,
        'author': author,
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'recipes/profile.html', context)


@login_required
def follow_list(request):
    author_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(author_list, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/follow_list.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def favorite_list(request):
    tags = get_tags(request)
    all_tags = Tag.objects.all()

    recipes = (
        Recipe.objects.by_tags(tags).params_for_query(request.user).filter(is_favorite=True)
    )

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': all_tags,
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'recipes/favorite_list.html', context)


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
    return render(request, 'recipes/purchase_list.html', context)


@login_required
def download_purchase_list(request):
    purchase_list = (RecipeIngredient.objects
                     .filter(recipe__shopping_list__user=request.user)
                     .values('ingredient__title', 'ingredient__dimension')
                     .annotate(Sum('quantity')))
    result = []
    file_data = ''
    if purchase_list:
        for ingredient in purchase_list:
            item = (f'{ingredient["ingredient__title"]} '
                    f'{ingredient["quantity__sum"]} '
                    f'{ingredient["ingredient__dimension"]}')
            result.append(item)
        file_data = '\n'.join(result)

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
