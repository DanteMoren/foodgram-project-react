from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models.constraints import UniqueConstraint
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        unique=True,
        help_text='Дайте короткое название тегу.'
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        help_text=('Укажите цвет для тега в формате HEX.')
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания.')
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=100,
        help_text=('Укажите название ингредиента.')
    )

    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=100,
        help_text=('Укажите единицу измерения ингредиента.')
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=255,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    image = models.ImageField()
    favorite_this = models.ManyToManyField(
        User,
        blank=True,
        related_name='favourite_recipes',
        verbose_name='Кому понравилось'
    )
    shopping_carts = models.ManyToManyField(
        User,
        blank=True,
        related_name='shopping_carts',
        verbose_name='Кто хочет купить'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name[:50]}, {self.author.username}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingrediens_in_recipe',
        verbose_name='Ингредиент в рецепте'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='related_ingredients_with_amount',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=0,
                message='Количество ингредиентов не может быть меньше 0')
        ],
        verbose_name='Количество'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_in_recipe'
            )
        ]
        verbose_name = 'Ingredient recipe'
        verbose_name_plural = 'Ingredients recipes'

    def __str__(self):
        return f'{self.recipe.name}, {self.ingredient.name}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow'
        )
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
