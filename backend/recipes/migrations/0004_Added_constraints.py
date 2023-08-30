from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0003_Tag_model_created_from_NameModel'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorites'
            ),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shopping_cart'
            ),
        ),
    ]
