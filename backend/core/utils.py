from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api import serializers
from recipes.models import IngredientInRecipe, Recipe


def checking_availability(user, object, model):
    if user.is_anonymous:
        return False
    return model.objects.filter(
        user=user,
        recipe=object.id,
    ).exists()


def add_delete_object(request, pk, model, text):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    filtered_data = model.objects.filter(user=user, recipe=recipe)
    if request.method == 'POST':
        if filtered_data.exists():
            return Response(
                {'error': f'Рецепт уже добавлен в {text}!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.RecipeInActionSerializer(
            recipe,
            context={'request': request},
        ).data
        model.objects.create(user=user, recipe=recipe)
        return Response(serializer, status=status.HTTP_201_CREATED)
    if filtered_data.exists():
        filtered_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'error': f'Рецепт ещё не добавляли в {text}!'},
        status=status.HTTP_400_BAD_REQUEST,
    )


def add_tags_and_ingredients(tags, ingredients, model):
    model.tags.set(tags)
    IngredientInRecipe.objects.bulk_create(
        [
            IngredientInRecipe(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ],
    )
