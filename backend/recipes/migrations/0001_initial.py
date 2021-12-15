# Generated by Django 3.2.9 on 2021-12-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Дайте короткое название тегу', max_length=200, unique=True, verbose_name='Заголовок')),
                ('color', models.CharField(help_text='Укажите цвет для тега в формате HEX', max_length=7, unique=True)),
                ('slug', models.SlugField(help_text='Укажите адрес для страницы задачи. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', max_length=200, unique=True, verbose_name='Слаг')),
            ],
        ),
    ]