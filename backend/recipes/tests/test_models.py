import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from mixer.backend.django import mixer

from core.utils import cut_string
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class TagsModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = mixer.blend('recipes.Tag')

    def test_tag_correct_def_str(self) -> None:
        """Проверяем, что у модели Tag корректно работает __str__."""
        self.assertEqual(cut_string(self.tag.name), str(self.tag))

    def test_tag_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Tag совпадают с ожидаемыми."""
        field_verboses = {
            'name': 'название',
            'color': 'цвет в HEX',
            'slug': 'слаг',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Tag._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_tag_correct_help_text(self) -> None:
        """help_text в полях модели Tag совпадают с ожидаемыми."""
        field_help_texts = {
            'name': 'Введите название',
            'color': 'Введите цвет',
            'slug': 'Введите слаг',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Tag._meta.get_field(value).help_text,
                    expected,
                )


class IngredientsModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.ingredient = mixer.blend('recipes.Ingredient')

    def test_ingredient_correct_def_str(self) -> None:
        """Проверяем, что у модели Ingredient корректно работает __str__."""
        self.assertEqual(
            cut_string(self.ingredient.name),
            str(self.ingredient),
        )

    def test_ingredient_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Ingredient совпадают с ожидаемыми."""
        field_verboses = {
            'name': 'название',
            'measurement_unit': 'единица измерения',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Ingredient._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_ingredient_correct_help_text(self) -> None:
        """help_text в полях модели Ingredient совпадают с ожидаемыми."""
        field_help_texts = {
            'name': 'Введите название',
            'measurement_unit': 'Введите единицу измерения',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Ingredient._meta.get_field(value).help_text,
                    expected,
                )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipesModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.recipe = mixer.blend('recipes.Recipe')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_recipe_correct_def_str(self) -> None:
        """Проверяем, что у модели Recipe корректно работает __str__."""
        self.assertEqual(cut_string(self.recipe.name), str(self.recipe))

    def test_recipe_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Recipe совпадают с ожидаемыми."""
        field_verboses = {
            'name': 'название',
            'tags': 'список тегов',
            'author': 'автор',
            'image': 'картинка',
            'text': 'описание',
            'ingredients': 'список ингредиентов',
            'cooking_time': 'время приготовления (в минутах)',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Recipe._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_recipe_correct_help_text(self) -> None:
        """help_text в полях модели Recipe совпадают с ожидаемыми."""
        field_help_texts = {
            'name': 'Введите название',
            'tags': 'Выберите теги',
            'author': 'Выберите автора',
            'image': 'Выберите картинку',
            'text': 'Введите описание рецепта',
            'ingredients': 'Выберите ингредиенты',
            'cooking_time': 'Введите время приготовления (в минутах)',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Recipe._meta.get_field(value).help_text,
                    expected,
                )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class IngredientsInRecipesModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.ingredient_in_recipe = mixer.blend('recipes.IngredientInRecipe')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_ingredient_in_recipe_correct_def_str(self) -> None:
        """
        Проверяем, что у модели IngredientInRecipe корректно работает __str__.
        """
        self.assertEqual(
            (
                f'Рецепт `{self.ingredient_in_recipe.recipe}` содержит'
                f' `{self.ingredient_in_recipe.ingredient}`'
            ),
            str(self.ingredient_in_recipe),
        )

    def test_ingredient_in_recipe_correct_verbose_name(self) -> None:
        """
        verbose_name в полях модели IngredientInRecipe совпадают с ожидаемыми.
        """
        field_verboses = {
            'recipe': 'рецепт',
            'ingredient': 'ингредиент',
            'amount': 'количество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    IngredientInRecipe._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_ingredient_in_recipe_correct_help_text(self) -> None:
        """
        help_text в полях модели IngredientInRecipe совпадают с ожидаемыми.
        """
        field_help_texts = {
            'recipe': 'Выберите рецепт',
            'ingredient': 'Выберите ингредиент',
            'amount': 'Введите количество ингредиентов',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    IngredientInRecipe._meta.get_field(value).help_text,
                    expected,
                )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FavoritsModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.favorite = mixer.blend('recipes.Favorite')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_favorite_correct_def_str(self) -> None:
        """Проверяем, что у модели Favorite корректно работает __str__."""
        self.assertEqual(
            (
                f'`{self.favorite.user}` добавил в избранное'
                f' `{self.favorite.recipe}`'
            ),
            str(self.favorite),
        )

    def test_favorite_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Favorite совпадают с ожидаемыми."""
        field_verboses = {
            'user': 'пользователь',
            'recipe': 'рецепт',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Favorite._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_favorite_correct_help_text(self) -> None:
        """help_text в полях модели Favorite совпадают с ожидаемыми."""
        field_help_texts = {
            'user': (
                'Выберите пользователя, который добавляет рецепт в избранное'
            ),
            'recipe': 'Выберите рецепт',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Favorite._meta.get_field(value).help_text,
                    expected,
                )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ShoppingCartsModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.shopping_cart = mixer.blend('recipes.ShoppingCart')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_shopping_cart_correct_def_str(self) -> None:
        """Проверяем, что у модели ShoppingCart корректно работает __str__."""
        self.assertEqual(
            (
                f'`{self.shopping_cart.user}` добавил в список'
                f' покупок `{self.shopping_cart.recipe}`'
            ),
            str(self.shopping_cart),
        )

    def test_shopping_cart_correct_verbose_name(self) -> None:
        """verbose_name в полях модели ShoppingCart совпадают с ожидаемыми."""
        field_verboses = {
            'user': 'пользователь',
            'recipe': 'рецепт',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    ShoppingCart._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_shopping_cart_correct_help_text(self) -> None:
        """help_text в полях модели ShoppingCart совпадают с ожидаемыми."""
        field_help_texts = {
            'user': (
                'Выберите пользователя, который добавляет рецепт в'
                ' список покупок'
            ),
            'recipe': 'Выберите рецепт',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    ShoppingCart._meta.get_field(value).help_text,
                    expected,
                )
