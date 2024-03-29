from django import template

from recipes.models import Tag

register = template.Library()


@register.filter()
def tag_id(tag_title):
    id = Tag.objects.filter(title=tag_title).values_list('id', flat=True)[0]
    return id


@register.filter()
def tag_color(tag_title):
    color = Tag.objects.filter(
        title=tag_title
    ).values_list('color', flat=True)[0]
    return color


@register.simple_tag
def more_recipes(more, per_page):
    values = ['рецепт', 'рецепта', 'рецептов']
    value = ''
    more = more-per_page
    number = abs(int(more))
    a = number % 10
    b = number % 100
    if more > 0:
        if (a == 1) and (b != 11):
            value = values[0]
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            value = values[1]
        else:
            value = values[2]
        return f'Еще {more} {value}'
    return 'Посмотреть профиль'


@register.simple_tag
def get_params(url, tag):
    if '?' in url:
        return f'{url}&tags={tag}'
    return f'{url}?tags={tag}'


@register.simple_tag
def remove_get_params(request, tags=None, param=''):
    tags = list(tags)
    tags.remove(param)
    params = '&'.join(f'tags={tag}' for tag in tags)
    if 'page' in request.GET:
        path = str(request.get_full_path())
        params_page = path.split('&')
        if len(params) > 0:
            return f'{params_page[0]}&{params}'
        else:
            return f'{params_page[0]}'
    return f'?{params}'


@register.simple_tag
def switch_page(request, page_number):
    path = request.get_full_path()
    current_page = request.GET.get('page')
    if 'tags' in path and 'page' in path:
        return path.replace(f'page={current_page}', f'page={page_number}')
    if 'tags' in path and 'page' not in path:
        return f'?page={page_number}&{path[2:]}'
    return f'?page={page_number}'
