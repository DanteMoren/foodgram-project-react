# Generated by Django 3.2.9 on 2021-12-13 06:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0016_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='favorite_this',
            field=models.ManyToManyField(blank=True, null=True, related_name='favourite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Кому понравилось'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='shopping_carts',
            field=models.ManyToManyField(blank=True, null=True, related_name='shopping_carts', to=settings.AUTH_USER_MODEL, verbose_name='Кто хочет купить'),
        ),
    ]