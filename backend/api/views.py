from rest_framework import filters

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeReadOnlySerializer,
)
from api.mixins import ListRetrieveAPIView, CRUDAPIView
from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe
from core.paginations import RecipesPagination


class TagAPIView(ListRetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientAPIView(ListRetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesAPIView(CRUDAPIView):
    queryset = Recipe.objects.all()
    pagination_class = RecipesPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadOnlySerializer
        return RecipeSerializer
