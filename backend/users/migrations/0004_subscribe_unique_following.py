# Generated by Django 3.2.3 on 2023-08-17 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_subscribe'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(
                fields=('user', 'following'), name='unique_following'
            ),
        ),
    ]
