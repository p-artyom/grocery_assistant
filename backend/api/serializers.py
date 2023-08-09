from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
