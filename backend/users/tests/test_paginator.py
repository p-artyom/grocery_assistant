from django.conf import settings
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import User


class UsersPaginatorTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = mixer.blend(User)
        cls.subscribe = mixer.cycle(14).blend(
            'users.Subscribe',
            user=cls.user,
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)

    def test_paginator(self) -> None:
        """На страницу подписок передаётся ожидаемое количество объектов."""
        urls_num_objects = (
            ('/api/users/subscriptions/', settings.NUM_OBJECTS_ON_PAGE),
            (
                '/api/users/subscriptions/?page=2',
                settings.NUM_OBJECTS_ON_PAGE,
            ),
            (
                '/api/users/subscriptions/?page=3',
                settings.NUM_OBJECTS_ON_LAST_PAGE_FOR_TEST,
            ),
        )
        for url, num_object in urls_num_objects:
            with self.subTest(url=url, num_object=num_object):
                self.assertEqual(
                    len(self.authorized_user.get(url).json()['results']),
                    num_object,
                )
