# Generated by Django 3.2.3 on 2023-08-18 07:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                help_text='Выберите автора',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        help_text='Выберите рецепт',
                        on_delete=django.db.models.deletion.CASCADE,
                        to='recipes.recipe',
                        verbose_name='рецепт',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='Выберите пользователя, который добавляет в избранное',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
            },
        ),
    ]