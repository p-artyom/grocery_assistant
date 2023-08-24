import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase, override_settings
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipesUrlsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, cls.author = mixer.cycle(2).blend(User)

        cls.tag = mixer.blend('recipes.Tag')
        cls.ingredient = mixer.blend('recipes.Ingredient')
        cls.recipe = mixer.blend(
            'recipes.Recipe',
            tags=cls.tag,
            author=cls.author,
            ingredients=cls.ingredient,
        )
        cls.shopping_cart = mixer.blend(
            'recipes.ShoppingCart',
            user=cls.author,
            recipe=cls.recipe,
        )
        cls.favorite = mixer.blend(
            'recipes.Favorite',
            user=cls.author,
            recipe=cls.recipe,
        )

        cls.cooking_time = 15
        cls.amount = 10
        cls.name = 'Карамельный латте'
        cls.updated_name = 'Латте с корицей'
        cls.text = 'Кофе с пеной взбитых сливок и ароматом карамели'
        cls.updated_text = 'Кофе и корица - отличное сочетание'
        cls.image = (
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAA'
            'ABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
            'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAA'
            'BJRU5ErkJggg=='
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()
        cls.author_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)
        cls.author_user.force_authenticate(cls.author)

        cls.urls = {
            'tags': '/api/tags/',
            'tag': f'/api/tags/{cls.tag.id}/',
            'unknown_tag': '/api/tags/99/',
            'ingredients': '/api/ingredients/',
            'ingredient': f'/api/ingredients/{cls.ingredient.id}/',
            'unknown_ingredient': '/api/ingredients/99/',
            'recipes': '/api/recipes/',
            'recipe': f'/api/recipes/{cls.recipe.id}/',
            'unknown_recipe': '/api/recipes/99/',
            'download': '/api/recipes/download_shopping_cart/',
            'shoping_cart': f'/api/recipes/{cls.recipe.id}/shopping_cart/',
            'favorite': f'/api/recipes/{cls.recipe.id}/favorite/',
        }

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_http_statuses_get_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при GET запросах."""
        urls_statuses_users = (
            (self.urls.get('tags'), HTTPStatus.OK, self.client),
            (self.urls.get('tag'), HTTPStatus.OK, self.client),
            (self.urls.get('unknown_tag'), HTTPStatus.NOT_FOUND, self.client),
            (self.urls.get('ingredients'), HTTPStatus.OK, self.client),
            (self.urls.get('ingredient'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unknown_ingredient'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (self.urls.get('recipes'), HTTPStatus.OK, self.client),
            (self.urls.get('recipe'), HTTPStatus.OK, self.client),
            (
                self.urls.get('unknown_recipe'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (self.urls.get('download'), HTTPStatus.OK, self.author_user),
            (
                self.urls.get('download'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
        )
        for url, status, user in urls_statuses_users:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(user.get(url).status_code, status)

    def test_http_statuses_post_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при POST запросах."""
        urls_statuses_users_data = (
            (
                self.urls.get('recipes'),
                HTTPStatus.CREATED,
                self.authorized_user,
                {
                    'tags': [self.tag.id],
                    'ingredients': [
                        {'id': self.ingredient.id, 'amount': self.amount},
                    ],
                    'image': self.image,
                    'name': self.name,
                    'text': self.text,
                    'cooking_time': self.cooking_time,
                },
            ),
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.CREATED,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.BAD_REQUEST,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.CREATED,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.BAD_REQUEST,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
        )
        for url, status, user, data in urls_statuses_users_data:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.post(url, data=data, format='json').status_code,
                    status,
                )

    def test_http_statuses_patch_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при PATCH запросах."""
        urls_statuses_users_data = (
            (
                self.urls.get('recipe'),
                HTTPStatus.OK,
                self.author_user,
                {
                    'tags': [self.tag.id],
                    'ingredients': [
                        {'id': self.ingredient.id, 'amount': self.amount},
                    ],
                    'image': self.image,
                    'name': self.updated_name,
                    'text': self.updated_text,
                    'cooking_time': self.cooking_time,
                },
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.BAD_REQUEST,
                self.author_user,
                {
                    'tagsss': [self.tag.id],
                    'ingredientsss': [
                        {'id': self.ingredient.id, 'amount': self.amount},
                    ],
                    'image': self.image,
                    'name': self.updated_name,
                    'text': self.updated_text,
                    'cooking_time': self.cooking_time,
                },
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.BAD_REQUEST,
                self.author_user,
                {},
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.FORBIDDEN,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('unknown_recipe'),
                HTTPStatus.NOT_FOUND,
                self.authorized_user,
                {},
            ),
        )
        for url, status, user, data in urls_statuses_users_data:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.patch(url, data=data, format='json').status_code,
                    status,
                )

    def test_http_statuses_delete_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при DELETE запросах."""
        urls_statuses_users = (
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.NO_CONTENT,
                self.author_user,
            ),
            (
                self.urls.get('shoping_cart'),
                HTTPStatus.BAD_REQUEST,
                self.author_user,
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.NO_CONTENT,
                self.author_user,
            ),
            (
                self.urls.get('favorite'),
                HTTPStatus.BAD_REQUEST,
                self.author_user,
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.FORBIDDEN,
                self.authorized_user,
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.NO_CONTENT,
                self.author_user,
            ),
            (
                self.urls.get('recipe'),
                HTTPStatus.NOT_FOUND,
                self.author_user,
            ),
        )
        for url, status, user in urls_statuses_users:
            with self.subTest(
                url=url,
                status=status,
                user=user,
            ):
                self.assertEqual(
                    user.delete(url).status_code,
                    status,
                )
