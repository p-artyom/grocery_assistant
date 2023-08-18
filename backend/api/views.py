from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete
from api.serializers import (
    IngredientSerializer,
    RecipeInActionSerializer,
    RecipeReadOnlySerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.paginations import RecipePagination
from recipes.models import Favorite, Ingredient, Recipe, Tag


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

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if favorite.exists():
                return Response(
                    {'error': 'Рецепт уже добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = RecipeInActionSerializer(
                recipe,
                context={'request': request},
            ).data
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Рецепт ещё не добавляли в избранное!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
