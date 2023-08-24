from http import HTTPStatus

from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from users.models import User


class UsersUrlsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # cls.user, cls.author = mixer.cycle(2).blend(User)
        # cls.user = mixer.blend('users.User')
        cls.author = mixer.blend('users.User')

        cls.recipe = mixer.blend('users.Subscribe', user=cls.author)

        cls.email = 'guido@mail.ru'
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

        # cls.authorized_user.force_authenticate(user=cls.user)
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

    def test_http_statuses_post_request(self) -> None:
        """URL-адрес возвращает соответствующий статус при POST запросах."""
        data = {
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
        }
        self.assertEqual(
            self.client.post(
                self.urls.get('users'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.CREATED,
        )
        data = {
            'email': self.email,
            'usernameee': self.username,
            'first_nameeee': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
        }
        self.assertEqual(
            self.client.post(
                self.urls.get('users'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.BAD_REQUEST,
        )
        data = {
            'email': self.email,
            'password': self.password,
        }
        self.assertEqual(
            self.client.post(
                self.urls.get('login'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.OK,
        )
        user = User.objects.get(username=self.username)
        self.authorized_user.force_authenticate(user=user)
        data = {
            'new_password': self.new_password,
            'current_password': self.password,
        }
        self.assertEqual(
            self.authorized_user.post(
                self.urls.get('password'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.NO_CONTENT,
        )
        data = {
            'new_passworddd': self.new_password,
            'current_passworddd': self.password,
        }
        self.assertEqual(
            self.authorized_user.post(
                self.urls.get('password'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.BAD_REQUEST,
        )
        self.assertEqual(
            self.client.post(
                self.urls.get('password'),
                format='json',
            ).status_code,
            HTTPStatus.UNAUTHORIZED,
        )
        self.assertEqual(
            self.authorized_user.post(
                self.urls.get('logout'),
                data=data,
                format='json',
            ).status_code,
            HTTPStatus.NO_CONTENT,
        )
        self.assertEqual(
            self.client.post(
                self.urls.get('logout'),
                format='json',
            ).status_code,
            HTTPStatus.UNAUTHORIZED,
        )
        self.assertEqual(
            self.authorized_user.post(
                self.urls.get('subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.CREATED,
        )
        self.assertEqual(
            self.authorized_user.post(
                f'/api/users/{user.id}/subscribe/',
                format='json',
            ).status_code,
            HTTPStatus.BAD_REQUEST,
        )
        self.assertEqual(
            self.client.post(
                self.urls.get('subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.UNAUTHORIZED,
        )
        self.assertEqual(
            self.authorized_user.post(
                self.urls.get('unknown_subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.NOT_FOUND,
        )
        self.assertEqual(
            self.authorized_user.delete(
                self.urls.get('subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.NO_CONTENT,
        )
        self.assertEqual(
            self.authorized_user.delete(
                self.urls.get('subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.BAD_REQUEST,
        )
        self.assertEqual(
            self.client.delete(
                self.urls.get('subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.UNAUTHORIZED,
        )
        self.assertEqual(
            self.authorized_user.delete(
                self.urls.get('unknown_subscribe'),
                format='json',
            ).status_code,
            HTTPStatus.NOT_FOUND,
        )
