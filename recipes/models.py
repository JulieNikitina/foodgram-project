from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.TextField('наименование ингредиента', max_length=150)
    dimension = models.TextField('единицы измерения', max_length=10)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    title = models.CharField('название тега', max_length=50, db_index=True)
    display_name = models.CharField('название тега для шаблона', max_length=50)
    color = models.CharField('цвет тега', max_length=50)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class RecipeCustomQuerySet(models.QuerySet):
    def params_for_query(self, user):
        if user.is_anonymous:
            return self
        purchase = Purchase.objects.filter(
            recipe=models.OuterRef('pk'), user=user
        )
        favorite = Favorite.objects.filter(
            recipe=models.OuterRef('pk'), user=user
        )
        follow = Follow.objects.filter(
            author=models.OuterRef('author'), user=user
        )
        return self.annotate(
            is_purchase=models.Exists(purchase),
            is_favorite=models.Exists(favorite),
            is_follow=models.Exists(follow),
        )

    def by_tags(self, tags):
        if not tags:
            return self
        return self.filter(tags__title__in=tags).distinct()


class Recipe(models.Model):
    name = models.TextField('название', max_length=30, blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True, null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение',
    )
    slug = AutoSlugField(populate_from='name', allow_unicode=True, unique=True,
                         editable=True, verbose_name='slug')
    recipe_text = models.TextField('рецепт', null=False, blank=False)
    time_for_cooking = models.PositiveSmallIntegerField(
        'время приготовления',
        validators=[MinValueValidator(1, 'Так быстро не готовит даже Флэш')]
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    objects = RecipeCustomQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}: {self.recipe_text[0:10]}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts'
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'Значение должно быть больше нуля')]
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipe}:{self.ingredient}'


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
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user}:{self.author}'


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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user}:{self.recipe}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_list',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_list',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['user', 'recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
