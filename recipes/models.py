from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(blank=False, unique=True)
    title = models.CharField(
        blank=False,
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    name = models.TextField('название', max_length=30, blank=False, null=False)
    image = models.ImageField(
        upload_to='recipes/',
        blank=True, null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение',
    )
    recipe_text = models.TextField('рецепт', null=False, blank=False)
    # переделать на множественное поле
    ingredients = models.TextField('ингредиенты', max_length=500, null=True)
    # переделать на выбор в несколько категорий
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='recipes',
                                 verbose_name='категория'
                                 )

    time_for_cooking = models.TextField('время приготовления')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        name = self.name
        cut_text = self.recipe_text[0:10]
        return f'{name}: {cut_text}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ['user', 'author']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite'
    )

    class Meta:
        unique_together = ['user', 'recipe']



# class Comment(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='comments',
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments',
#     )
#     text = models.TextField('текст', help_text='Напишите ваш комментарий')
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         date = self.created
#         author = self.author
#         cut_text = self.text[0:10]
#         return f'{author}.{date}.{cut_text}'