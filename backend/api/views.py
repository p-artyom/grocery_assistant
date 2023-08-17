from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete
from api.serializers import (
    IngredientSerializer,
    RecipeReadOnlySerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.paginations import RecipePagination
from recipes.models import Ingredient, Recipe, Tag


class TagAPIView(ListRetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientAPIView(ListRetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeAPIView(CRUDAPIView):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorCanEditAndDelete,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadOnlySerializer
        return RecipeSerializer
