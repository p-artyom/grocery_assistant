from rest_framework import generics

from api.serializers import TagSerializer
from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe


class TagAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
