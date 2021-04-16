from recipes.models import Tag


def all_tags(request):
    return {
        'all_tags': Tag.objects.all()
    }


def tags(request):
    tags = request.GET.getlist('tags')
    return {
        'tags': tags
    }
