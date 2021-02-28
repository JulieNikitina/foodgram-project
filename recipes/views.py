from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category, User, Follow
from .forms import RecipeForm


def index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    button = True
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'button': button},
    )


def category_recipes(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=category).order_by('-pub_date')[:12]
    return render(request, 'category.html', {'category': category, 'recipes': recipes})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(
        request,
        'recipe.html',
        {
            'recipe': recipe,
            'author': recipe.author,
        }
    )


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    user = request.user
    if user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect('recipe', username, recipe_id)
    return render(request, 'new.html', {'form': form, 'recipe': recipe})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.count()
    user = request.user
    paginator = Paginator(author.recipes.all(), 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'profile.html', context)


@login_required
def follow_list(request):
    author_list = User.objects.filter(following__user=request.user)
    recipes_by_author = Recipe.objects.order_by('author')
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow_list.html',
        {'page': page, 'paginator': paginator, 'recipes_by_author': recipes_by_author}
    )


@login_required
def favorite_list(request):
    favorites = Recipe.objects.filter(recipe_favorite__user=request.user)
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite_list.html',
        {'page': page, 'paginator': paginator}
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


