import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user
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

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()
        cls.author_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)
        cls.author_user.force_authenticate(cls.author)

        cls.urls = {
            'tags': '/api/tags/',
            'first_tag': '/api/tags/1/',
            'second_tag': '/api/tags/2/',
            'ingredients': '/api/ingredients/',
            'first_ingredient': '/api/ingredients/1/',
            'second_ingredient': '/api/ingredients/2/',
            'recipes': '/api/recipes/',
            'first_recipe': '/api/recipes/1/',
            'second_recipe': '/api/recipes/2/',
        }

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_http_statuses_get_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при GET запросах."""
        url_status_user = (
            (self.urls.get('tags'), HTTPStatus.OK, self.client),
            (self.urls.get('first_tag'), HTTPStatus.OK, self.client),
            (self.urls.get('second_tag'), HTTPStatus.NOT_FOUND, self.client),
            (self.urls.get('ingredients'), HTTPStatus.OK, self.client),
            (self.urls.get('first_ingredient'), HTTPStatus.OK, self.client),
            (
                self.urls.get('second_ingredient'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
            (self.urls.get('recipes'), HTTPStatus.OK, self.client),
            (self.urls.get('first_recipe'), HTTPStatus.OK, self.client),
            (
                self.urls.get('second_recipe'),
                HTTPStatus.NOT_FOUND,
                self.client,
            ),
        )
        for url, status, user in url_status_user:
            with self.subTest(
                url=url,
                status=status,
                user=get_user(user).username,
            ):
                self.assertEqual(user.get(url).status_code, status)

    def test_http_statuses_post_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при POST запросах."""
        url_status_user_data = (
            (
                self.urls.get('recipes'),
                HTTPStatus.CREATED,
                self.authorized_user,
                {
                    'tags': [self.tag.id],
                    'ingredients': [
                        {'id': self.ingredient.id, 'amount': 10},
                    ],
                    'image': (
                        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAA'
                        'ABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
                        'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAA'
                        'BJRU5ErkJggg=='
                    ),
                    'name': 'Тестовый рецепт',
                    'text': 'Описание',
                    'cooking_time': 15,
                },
            ),
        )
        for url, status, user, data in url_status_user_data:
            with self.subTest(
                url=url,
                status=status,
                user=get_user(user).username,
            ):
                self.assertEqual(
                    user.post(url, data=data, format='json').status_code,
                    status,
                )
