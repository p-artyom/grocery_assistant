from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.models import NameModel
from core.utils import cut_string

User = get_user_model()


class Tag(NameModel):
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField('слаг', unique=True, help_text='Введите слаг')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return cut_string(self.name)


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


class Recipe(NameModel):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='список тегов',
        help_text='Теги, к которым относиться рецепт',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/',
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
        help_text='Ингредиенты, которые относяться к рецепту',
    )
    cooking_time = models.IntegerField(
        'время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
        help_text='Введите время приготовления (в минутах)',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return cut_string(self.name)


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        help_text='Количество ингредиентов',
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
