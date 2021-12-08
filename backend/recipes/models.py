from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank = False,
        null = False,
        unique=True,
        help_text='Дайте короткое название тегу.'
        )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        blank = False,
        null = False,
        unique=True,
        help_text=('Укажите цвет для тега в формате HEX.')
        )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        blank = False,
        null = False,
        unique=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания.')
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length = 100,
        blank = False,
        null = False,
        help_text=('Укажите название ингредиента.')
    )

    measurement_unit = models.CharField(
        verbose_name='Единица измерения',

        max_length = 100,
        blank = False,
        null = False,
        help_text=('Укажите единицу измерения ингредиента.')
    )
    
    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=255,
        blank=False,
        null= False,
        )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
        )
    text = models.TextField(
        verbose_name='Текстовое описание',
        blank=False,
        null=False,
    )

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        blank=False,
        null=False,
    )
    image = models.ImageField(
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return f'{self.name[:50]}, {self.author.username}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_with_amount',
        )
    amount = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.recipe.name}, {self.ingredient.name}'

# class IngredientRecipe(models.Model):
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE,
#         related_name="ingredients_amount",
#         verbose_name="Ингредиент"
#     )
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE,
#         related_name="ingredients_amount",
#         verbose_name="Рецепт"
#     )
#     amount = models.PositiveSmallIntegerField(
#         blank=False,
#         # validators=[
#         #     MinValueValidator(limit_value=0, message="Количество не может быть меньше 0")
#         # ],
#         verbose_name="Количество"
#     )

#     # class Meta:
#     #     verbose_name = "Количество ингредиента"
#     #     verbose_name_plural = "Количества ингредиентов"

#     def __str__(self):
#         return f'{self.recipe.name}, {self.ingredient.name}'