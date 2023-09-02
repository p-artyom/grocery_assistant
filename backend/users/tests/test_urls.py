from http import HTTPStatus

from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import User


class UsersUrlsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = mixer.blend('users.User')

        cls.subscribe = mixer.blend('users.Subscribe', user=cls.author)

        cls.email = 'guido@mail.ru'
        cls.unknown_email = 'rossum@mail.ru'
        cls.username = 'guido'
        cls.first_name = 'Гвидо ван'
        cls.last_name = 'Россум'
        cls.password = 'GuidoRossum'
        cls.new_password = 'RossumGuido'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.authorized_user = APIClient()
        cls.author_user = APIClient()

        cls.author_user.force_authenticate(cls.author)

        cls.urls = {
            'users': '/api/users/',
            'user': f'/api/users/{cls.author.id}/',
            'unknown_user': '/api/users/99/',
            'me': '/api/users/me/',
            'password': '/api/users/set_password/',
            'login': '/api/auth/token/login/',
            'logout': '/api/auth/token/logout/',
            'subscriptions': '/api/users/subscriptions/',
            'subscribe': f'/api/users/{cls.author.id}/subscribe/',
            'unknown_subscribe': '/api/users/99/subscribe/',
        }

    def test_http_statuses_get_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при GET запросах."""
        urls_statuses_users = (
            (self.urls.get('users'), HTTPStatus.OK, self.author_user),
            (self.urls.get('users'), HTTPStatus.UNAUTHORIZED, self.client),
            (self.urls.get('user'), HTTPStatus.OK, self.author_user),
            (self.urls.get('user'), HTTPStatus.UNAUTHORIZED, self.client),
            (
                self.urls.get('unknown_user'),
                HTTPStatus.NOT_FOUND,
                self.author_user,
            ),
            (
                self.urls.get('me'),
                HTTPStatus.OK,
                self.author_user,
            ),
            (
                self.urls.get('me'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
            (
                self.urls.get('subscriptions'),
                HTTPStatus.OK,
                self.author_user,
            ),
            (
                self.urls.get('subscriptions'),
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

    def test_http_statuses_post_delete_request(self) -> None:
        """URL-адрес возвращает корректный статус.

        Статус, возвращаемый при POST и DELETE запросах на URL-адреса,
        соответствует документации.
        """
        urls_statuses_users_data = (
            (
                self.urls.get('users'),
                HTTPStatus.CREATED,
                self.client,
                {
                    'email': self.email,
                    'username': self.username,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'password': self.password,
                },
            ),
            (
                self.urls.get('users'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {
                    'email': self.email,
                    'usernameee': self.username,
                    'first_nameeee': self.first_name,
                    'last_name': self.last_name,
                    'password': self.password,
                },
            ),
            (
                self.urls.get('login'),
                HTTPStatus.OK,
                self.client,
                {
                    'email': self.email,
                    'password': self.password,
                },
            ),
            (
                self.urls.get('login'),
                HTTPStatus.BAD_REQUEST,
                self.client,
                {
                    'email': self.unknown_email,
                    'password': self.password,
                },
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
        user = User.objects.get(username=self.username)
        self.authorized_user.force_authenticate(user=user)
        urls_statuses_users_data = (
            (
                self.urls.get('password'),
                HTTPStatus.NO_CONTENT,
                self.authorized_user,
                {
                    'new_password': self.new_password,
                    'current_password': self.password,
                },
            ),
            (
                self.urls.get('password'),
                HTTPStatus.BAD_REQUEST,
                self.authorized_user,
                {
                    'new_passworddd': self.new_password,
                    'current_passworddd': self.password,
                },
            ),
            (
                self.urls.get('password'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
            (
                self.urls.get('logout'),
                HTTPStatus.NO_CONTENT,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('logout'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
            (
                self.urls.get('subscribe'),
                HTTPStatus.CREATED,
                self.authorized_user,
                {},
            ),
            (
                f'/api/users/{user.id}/subscribe/',
                HTTPStatus.BAD_REQUEST,
                self.authorized_user,
                {},
            ),
            (
                self.urls.get('subscribe'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
                {},
            ),
            (
                self.urls.get('unknown_subscribe'),
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
                    user.post(url, data=data, format='json').status_code,
                    status,
                )
        urls_statuses_users = (
            (
                self.urls.get('subscribe'),
                HTTPStatus.NO_CONTENT,
                self.authorized_user,
            ),
            (
                self.urls.get('subscribe'),
                HTTPStatus.BAD_REQUEST,
                self.authorized_user,
            ),
            (
                self.urls.get('subscribe'),
                HTTPStatus.UNAUTHORIZED,
                self.client,
            ),
            (
                self.urls.get('unknown_subscribe'),
                HTTPStatus.NOT_FOUND,
                self.authorized_user,
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
