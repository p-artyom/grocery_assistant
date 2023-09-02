from django.conf import settings
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import Subscribe, User


class UsersViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {
            'email': 'guido@mail.ru',
            'username': 'guido',
            'first_name': 'Гвидо ван',
            'last_name': 'Россум',
            'password': 'GuidoRossum',
        }

    def test_user_registration_works_correctly(self) -> None:
        """Регистрация пользователя работает корректно."""
        self.assertEqual(
            User.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.client.post('/api/users/', data=self.data, format='json')
        self.assertEqual(
            User.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )


class SubscribeViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, cls.author = mixer.cycle(2).blend(User)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()
        cls.author_user = APIClient()

        cls.authorized_user.force_authenticate(cls.user)
        cls.author_user.force_authenticate(cls.author)

    def test_authorized_user_can_subscribe_and_unsubscribe(self) -> None:
        """Подписки работают корректно.

        Авторизованный пользователь может подписываться на других
        пользователей и удалять их из подписок.
        """
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(f'/api/users/{self.author.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.delete(f'/api/users/{self.author.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_subscribe_yourself(self) -> None:
        """Нельзя подписаться на самого себя."""
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(f'/api/users/{self.user.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_anon_cannot_subscribe(self) -> None:
        """Анонимный пользователь не может подписаться."""
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.client.post(f'/api/users/{self.user.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_subscribe_on_non_existent_user(self) -> None:
        """Нельзя подписаться на несуществующего пользователя."""
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post('/api/users/99/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )

    def test_cannot_re_subscribe(self) -> None:
        """Нельзя повторно подписаться на пользователя."""
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ZERO_OBJECTS_FOR_TEST,
        )
        self.authorized_user.post(f'/api/users/{self.author.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
        self.authorized_user.post(f'/api/users/{self.author.id}/subscribe/')
        self.assertEqual(
            Subscribe.objects.count(),
            settings.CHECK_ONE_OBJECT_FOR_TEST,
        )
