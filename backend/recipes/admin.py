from django.contrib import admin

from core.admin import BaseAdmin
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'image',
        'cooking_time',
        'created',
        'modified',
        'in_favorited',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    readonly_fields = ('in_favorited',)
    search_fields = ('name',)

    def in_favorited(self, object):
        return Favorite.objects.filter(recipe=object).count()

    in_favorited.short_description = 'число добавлений в избранное'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(BaseAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = (
        'recipe',
        'ingredient',
    )
    search_fields = (
        'recipe',
        'ingredient',
    )


@admin.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    list_display = ('pk', '__str__')
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(BaseAdmin):
    list_display = ('pk', '__str__')
    search_fields = ('user',)
