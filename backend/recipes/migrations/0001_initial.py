import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите название',
                        max_length=200,
                        verbose_name='название',
                    ),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        help_text='Введите единицу измерения',
                        max_length=200,
                        verbose_name='единица измерения',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.IntegerField(
                        help_text='Введите количество ингредиентов',
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='количество',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ингредиент в рецепт',
                'verbose_name_plural': 'ингредиенты в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите название',
                        max_length=200,
                        verbose_name='название',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    'modified',
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    'image',
                    models.ImageField(
                        help_text='Выберите картинку',
                        upload_to='recipes/images/',
                        verbose_name='картинка',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        help_text='Введите описание рецепта',
                        verbose_name='описание',
                    ),
                ),
                (
                    'cooking_time',
                    models.IntegerField(
                        help_text='Введите время приготовления (в минутах)',
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='время приготовления (в минутах)',
                    ),
                ),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите название',
                        max_length=200,
                        unique=True,
                        verbose_name='название',
                    ),
                ),
                (
                    'color',
                    models.CharField(
                        help_text='Введите цвет',
                        max_length=7,
                        unique=True,
                        verbose_name='цвет в HEX',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Введите слаг',
                        unique=True,
                        verbose_name='слаг',
                    ),
                ),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        help_text='Выберите рецепт',
                        on_delete=django.db.models.deletion.CASCADE,
                        to='recipes.recipe',
                        verbose_name='рецепт',
                    ),
                ),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'список покупок',
            },
        ),
    ]
