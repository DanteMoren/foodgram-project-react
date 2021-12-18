from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Follow


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class IngredientsRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name', )


@admin.register(Recipe)
class Recipe(admin.ModelAdmin):
    inlines = (IngredientsRecipeInLine, )
    list_display = (
        'name',
        'author',
        'favorite_count',
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )

    @admin.display(description='Количество добавлений в избранное')
    def favorite_count(self, obj):
        return obj.favorite_this.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    list_filter = (
        'user',
    )
