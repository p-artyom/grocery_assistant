from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                help_text='Введите Email',
                max_length=254,
                unique=True,
                verbose_name='email',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(
                help_text='Введите имя', max_length=150, verbose_name='имя'
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(
                help_text='Введите фамилию',
                max_length=150,
                verbose_name='фамилия',
            ),
        ),
    ]
