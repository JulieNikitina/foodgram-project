from django import template

from recipes.models import Tag, Recipe, Favorite

register = template.Library()


@register.filter()
def tag_id(tag_title):
    id = Tag.objects.filter(title=tag_title).values_list('id', flat=True)[0]
    return id


@register.filter()
def tag_color(tag_title):
    color = Tag.objects.filter(title=tag_title).values_list('color', flat=True)[0]
    return color


@register.simple_tag
def recipes_by(author):
    return Recipe.objects.filter(author=author)[:3]


@register.simple_tag
def more_recipes(author):
    values = ['рецепт', 'рецепта', 'рецептов']
    value = ''
    count = Recipe.objects.all().count()
    more = count - 3
    number = abs(int(more))
    a = number % 10
    b = number % 100
    if more > 0:
        if (a == 1) and (b != 11):
            value = values[0]
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            value = values[1]
        else:
            value = values[1]
        return f'Еще {more} {value}'
    else:
        return ''


