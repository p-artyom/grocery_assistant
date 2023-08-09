from django.contrib import admin

from core.admin import BaseAdmin
from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'author', 'text')
    list_filter = ('author', 'name',)
    # list_editable = ('tags', 'ingredients',)
    search_fields = ('name',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(BaseAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient',)
    search_fields = ('recipe', 'ingredient',)