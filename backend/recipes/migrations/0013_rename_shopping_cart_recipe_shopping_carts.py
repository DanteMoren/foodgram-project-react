# Generated by Django 3.2.9 on 2021-12-08 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20211208_2108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='shopping_cart',
            new_name='shopping_carts',
        ),
    ]
