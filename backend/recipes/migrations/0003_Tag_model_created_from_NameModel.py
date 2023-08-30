from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(
                help_text='Введите название',
                max_length=200,
                verbose_name='название',
            ),
        ),
    ]
