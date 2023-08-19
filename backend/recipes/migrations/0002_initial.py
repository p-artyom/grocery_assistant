import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(
                help_text='Выберите пользователя, который добавляет рецепт в список покупок',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                help_text='Выберите автора',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                help_text='Выберите ингредиенты',
                through='recipes.IngredientInRecipe',
                to='recipes.Ingredient',
                verbose_name='список ингредиентов',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                help_text='Выберите теги',
                to='recipes.Tag',
                verbose_name='список тегов',
            ),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(
                help_text='Выберите ингредиент',
                on_delete=django.db.models.deletion.CASCADE,
                to='recipes.ingredient',
                verbose_name='ингредиент',
            ),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(
                help_text='Выберите рецепт',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ingredient_in_recipe',
                to='recipes.recipe',
                verbose_name='рецепт',
            ),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(
                help_text='Выберите рецепт',
                on_delete=django.db.models.deletion.CASCADE,
                to='recipes.recipe',
                verbose_name='рецепт',
            ),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(
                help_text='Выберите пользователя, который добавляет рецепт в избранное',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipe',
            constraint=models.UniqueConstraint(
                fields=('recipe', 'ingredient'), name='unique_ingredients'
            ),
        ),
    ]
