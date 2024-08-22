# Generated by Django 5.0.6 on 2024-08-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Запущен'), ('done', 'Завершена')], default='created', max_length=20, verbose_name='Статус'),
        ),
    ]
