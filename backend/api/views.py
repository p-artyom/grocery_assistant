from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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
from core.paginations import LimitPagination
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


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
    pagination_class = LimitPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorCanEditAndDelete,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadOnlySerializer
        return RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.action == 'list' or self.action == 'retrieve':
            is_favorited = self.request.query_params.get('is_favorited')
            if is_favorited is not None:
                queryset = (
                    queryset.filter(favorite__user=self.request.user)
                    if is_favorited == '1'
                    else queryset.filter(
                        ~Q(favorite__user=self.request.user),
                    )
                )
            is_in_shopping_cart = self.request.query_params.get(
                'is_in_shopping_cart',
            )
            if is_in_shopping_cart is not None:
                queryset = (
                    queryset.filter(shoppingcart__user=self.request.user)
                    if is_in_shopping_cart == '1'
                    else queryset.filter(
                        ~Q(shoppingcart__user=self.request.user),
                    )
                )
            tags = self.request.query_params.get('tags')
            if tags is not None:
                queryset = queryset.filter(tags__slug=tags)
        return queryset

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

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if shopping_cart.exists():
                return Response(
                    {'error': 'Рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = RecipeInActionSerializer(
                recipe,
                context={'request': request},
            ).data
            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(serializer, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Рецепт ещё не добавляли в список покупок!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=['GET'],
        detail=False,
    )
    def download_shopping_cart(self, request):
        return Response(
            {'error': 'Работаем над этим!'},
            status=status.HTTP_400_BAD_REQUEST,
        )
