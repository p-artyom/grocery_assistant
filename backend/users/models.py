from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email', unique=True, help_text='Введите Email')
    first_name = models.CharField(
        'имя',
        max_length=150,
        help_text='Введите имя',
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        help_text='Введите фамилию',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-id',)

    def __str__(self) -> str:
        return f'Создан пользователь `{self.email}`'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Введите пользователя, который оформляет подписку',
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Введите пользователя, на которого нужно оформить подписку',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following',
            ),
        ]

    def __str__(self) -> str:
        return f'`{self.user}` подписался на `{self.following}`'
