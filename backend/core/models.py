from django.db import models


class NameModel(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        help_text='Введите название',
    )

    class Meta:
        abstract = True
