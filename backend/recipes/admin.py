from django.contrib import admin

from .models import Tag, Ingredient, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name', )

@admin.register(Recipe)
class Recipe(admin.ModelAdmin):
    list_display = (
        'name',
        'author'
    )
    list_filter = (
        'author',
        'name',
        'tags'
        )