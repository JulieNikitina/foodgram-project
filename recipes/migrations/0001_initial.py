# Generated by Django 2.2 on 2021-03-19 02:19

import autoslug.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=150, verbose_name='наименование ингредиента')),
                ('dimension', models.TextField(max_length=10, verbose_name='единицы измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=30, verbose_name='название')),
                ('image', models.ImageField(blank=True, help_text='Загрузите изображение', null=True, upload_to='recipes/', verbose_name='Изображение')),
                ('slug', autoslug.fields.AutoSlugField(allow_unicode=True, editable=True, populate_from='title', unique=True, verbose_name='slug')),
                ('recipe_text', models.TextField(verbose_name='рецепт')),
                ('time_for_cooking', models.PositiveSmallIntegerField(verbose_name='время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='название тега')),
                ('display_name', models.CharField(max_length=50, verbose_name='название тега для шаблона')),
                ('color', models.CharField(max_length=50, verbose_name='цвет тега')),
            ],
            options={
                'verbose_name': 'тег',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=6, validators=[django.core.validators.MinValueValidator(1)])),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.Recipe')),
            ],
        ),
    ]
