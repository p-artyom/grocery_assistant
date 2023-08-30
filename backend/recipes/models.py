from behaviors.behaviors import Timestamped
from django.core.validators import MinValueValidator
from django.db import models

from core.models import NameModel
from recipes.utils import cut_string
from users.models import User


class Tag(NameModel):
    color = models.CharField(
        'цвет в HEX',
        max_length=7,
        unique=True,
        help_text='Введите цвет',
    )
    slug = models.SlugField('слаг', unique=True, help_text='Введите слаг')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return cut_string(self.name)

    def save(self, *args, **kwargs):
        self.color = self.color.upper()
        return super(Tag, self).save(*args, **kwargs)


class Ingredient(NameModel):
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=200,
        help_text='Введите единицу измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return cut_string(self.name)


class Recipe(NameModel, Timestamped):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='список тегов',
        help_text='Выберите теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Выберите автора',
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/images/',
        help_text='Выберите картинку',
    )
    text = models.TextField(
        'описание',
        help_text='Введите описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='список ингредиентов',
        help_text='Выберите ингредиенты',
    )
    cooking_time = models.IntegerField(
        'время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
        help_text='Введите время приготовления (в минутах)',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-created',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('created').verbose_name = 'дата публикации'
        self._meta.get_field('modified').verbose_name = 'дата изменения'

    def __str__(self) -> str:
        return cut_string(self.name)


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберите рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='Выберите ингредиент',
    )
    amount = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        help_text='Введите количество ингредиентов',
    )

    class Meta:
        verbose_name = 'ингредиент в рецепт'
        verbose_name_plural = 'ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients',
            ),
        ]

    def __str__(self):
        return f'Рецепт `{self.recipe}` содержит `{self.ingredient}`'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Выберите пользователя, который добавляет'
        ' рецепт в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберите рецепт',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorites',
            ),
        ]

    def __str__(self) -> str:
        return f'`{self.user}` добавил в избранное `{self.recipe}`'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Выберите пользователя, который добавляет'
        ' рецепт в список покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберите рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            ),
        ]

    def __str__(self) -> str:
        return f'`{self.user}` добавил в список покупок `{self.recipe}`'
