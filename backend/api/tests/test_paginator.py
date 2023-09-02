import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipesPaginatorTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = mixer.blend(User)
        cls.recipes = mixer.cycle(14).blend('recipes.Recipe')

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_paginator(self) -> None:
        """На страницу рецептов передаётся ожидаемое количество объектов."""
        urls_num_objects = (
            ('/api/recipes/', settings.NUM_OBJECTS_ON_PAGE),
            ('/api/recipes/?page=2', settings.NUM_OBJECTS_ON_PAGE),
            (
                '/api/recipes/?page=3',
                settings.NUM_OBJECTS_ON_LAST_PAGE_FOR_TEST,
            ),
        )
        for url, num_object in urls_num_objects:
            with self.subTest(url=url, num_object=num_object):
                self.assertEqual(
                    len(self.authorized_user.get(url).json()['results']),
                    num_object,
                )
