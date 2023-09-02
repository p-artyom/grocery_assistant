import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from recipes.models import Favorite, Recipe, ShoppingCart
from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipesViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = mixer.blend(User)

        cls.tag = mixer.blend('recipes.Tag')
        cls.ingredient = mixer.blend('recipes.Ingredient')

        cls.data = {
            'tags': [cls.tag.id],
            'ingredients': [
                {'id': cls.ingredient.id, 'amount': 10},
            ],
            'image': (
                'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAA'
                'ABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
                'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAA'
                'BJRU5ErkJggg=='
            ),
            'name': 'Карамельный латте',
            'text': 'Кофе с пеной взбитых сливок и ароматом карамели',
            'cooking_time': 15,
        }

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_authorized_user_can_add_and_delete_recipe(self) -> None:
        """Добавление рецепта работает корректно.

        Авторизованный пользователь может добавлять рецепт и удалять.
        """
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(
            '/api/recipes/',
            data=self.data,
            format='json',
        )
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.delete('/api/recipes/1/')
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_anon_cannot_add_recipe(self) -> None:
        """Анонимный пользователь не может добавить рецепт."""
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.client.post('/api/recipes/', data=self.data, format='json')
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_anon_cannot_delete_recipe(self) -> None:
        """Анонимный пользователь не может удалить рецепт."""
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(
            '/api/recipes/',
            data=self.data,
            format='json',
        )
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.client.delete('/api/recipes/1/')
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )

    def test_anon_cannot_delete_recipe(self) -> None:
        """Только автор рецепта может его удалить."""
        author = mixer.blend(User)
        author_user = APIClient()
        author_user.force_authenticate(author)
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        author_user.post('/api/recipes/', data=self.data, format='json')
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.delete('/api/recipes/1/')
        self.assertEqual(
            Recipe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )

    def test_authorized_user_can_add_and_delete_shopping_cart(self) -> None:
        """Добавление рецепта в список покупок работает корректно.

        Авторизованный пользователь может добавлять рецепт в список покупок
        и удалять.
        """
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(
            f'/api/recipes/{self.recipe.id}/shopping_cart/',
        )
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.delete(
            f'/api/recipes/{self.recipe.id}/shopping_cart/',
        )
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_anon_cannot_add_recipe_to_shopping_cart(self) -> None:
        """Анонимный пользователь не может добавить рецепт в список покупок."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.client.post(f'/api/recipes/{self.recipe.id}/shopping_cart/')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_add_shopping_cart_on_non_existent_recipe(self) -> None:
        """Нельзя добавить в список покупок несуществующий рецепт."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post('/api/recipes/99/shopping_cart/')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_re_add_recipe_to_shopping_cart(self) -> None:
        """Нельзя повторно добавить в список покупок рецепт."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(
            f'/api/recipes/{self.recipe.id}/shopping_cart/',
        )
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.post(
            f'/api/recipes/{self.recipe.id}/shopping_cart/',
        )
        self.assertEqual(
            ShoppingCart.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )

    def test_authorized_user_can_add_and_delete_favorite(self) -> None:
        """Добавление рецепта в избранное работает корректно.

        Авторизованный пользователь может добавлять рецепт в избранное
        и удалять.
        """
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.delete(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_anon_cannot_add_recipe_to_favorite(self) -> None:
        """Анонимный пользователь не может добавить рецепт в избранное."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.client.post(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_add_favorite_on_non_existent_recipe(self) -> None:
        """Нельзя добавить в избранное несуществующий рецепт."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post('/api/recipes/99/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_re_add_recipe_to_favorite(self) -> None:
        """Нельзя повторно добавить в избранное рецепт."""
        self.recipe = mixer.blend('recipes.Recipe')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.post(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(
            Favorite.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
