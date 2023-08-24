from django.test import TestCase
from mixer.backend.django import mixer

from users.models import Subscribe, User


class UsersModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = mixer.blend('users.User')

    def test_user_correct_def_str(self) -> None:
        """Проверяем, что у модели User корректно работает __str__."""
        self.assertEqual(
            f'Создан пользователь `{self.user.email}`',
            str(self.user),
        )

    def test_user_correct_verbose_name(self) -> None:
        """verbose_name в полях модели User совпадают с ожидаемыми."""
        field_verboses = {
            'email': 'email',
            'first_name': 'имя',
            'last_name': 'фамилия',
            'password': 'пароль',
            'username': 'имя пользователя',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    User._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_user_correct_help_text(self) -> None:
        """help_text в полях модели User совпадают с ожидаемыми."""
        field_help_texts = {
            'email': 'Введите Email',
            'first_name': 'Введите имя',
            'last_name': 'Введите фамилию',
            'username': (
                'Обязательное поле. Не более 150 символов. Только буквы,'
                ' цифры и символы @/./+/-/_.'
            ),
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    User._meta.get_field(value).help_text,
                    expected,
                )


class SubscribersModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.subscribe = mixer.blend('users.Subscribe')

    def test_subscribe_correct_def_str(self) -> None:
        """Проверяем, что у модели Subscribe корректно работает __str__."""
        self.assertEqual(
            (
                f'`{self.subscribe.user}` подписался на'
                f' `{self.subscribe.following}`'
            ),
            str(self.subscribe),
        )

    def test_subscribe_correct_verbose_name(self) -> None:
        """verbose_name в полях модели Subscribe совпадают с ожидаемыми."""
        field_verboses = {
            'user': 'пользователь',
            'following': 'автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Subscribe._meta.get_field(value).verbose_name,
                    expected,
                )

    def test_subscribe_correct_help_text(self) -> None:
        """help_text в полях модели Subscribe совпадают с ожидаемыми."""
        field_help_texts = {
            'user': 'Введите пользователя, который оформляет подписку',
            'following': (
                'Введите пользователя, на которого нужно оформить подписку'
            ),
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    Subscribe._meta.get_field(value).help_text,
                    expected,
                )
