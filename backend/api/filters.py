from recipes.models import Recipe
from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters


class TagsFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ['tags']
