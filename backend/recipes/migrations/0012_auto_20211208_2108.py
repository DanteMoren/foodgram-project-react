# Generated by Django 3.2.9 on 2021-12-08 18:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0011_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite_this',
            field=models.ManyToManyField(related_name='favourite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Кому понравилось'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='shopping_cart',
            field=models.ManyToManyField(related_name='shopping_carts', to=settings.AUTH_USER_MODEL, verbose_name='Кто хочет купить'),
        ),
    ]
