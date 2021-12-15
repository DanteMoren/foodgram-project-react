# Generated by Django 3.2.9 on 2021-12-08 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_rename_shopping_cart_recipe_shopping_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Количество ингредиентов не может быть меньше 0')], verbose_name='Количество'),
        ),
    ]
