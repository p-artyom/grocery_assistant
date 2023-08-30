import csv
from functools import reduce
from operator import or_

from django.db.models import Q, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.mixins import CRUDAPIView, ListRetrieveAPIView
from api.permissions import AuthorCanEditAndDelete
from api.serializers import (
    IngredientSerializer,
    RecipeReadOnlySerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.paginations import LimitPagination
from core.utils import add_delete_object
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


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
            tags = self.request.query_params.getlist('tags')
            if tags:
                queryset = queryset.filter(
                    reduce(or_, [Q(tags__slug=tag) for tag in tags]),
                ).distinct()
        return queryset

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
    )
    def favorite(self, request, pk):
        return add_delete_object(request, pk, Favorite, 'избранное')

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        return add_delete_object(request, pk, ShoppingCart, 'список покупок')

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        recipe = ShoppingCart.objects.filter(user=user).values('recipe')
        if not recipe.exists():
            return Response(
                {'error': 'Список покупок пуст!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__in=recipe,
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total=Sum('amount'))
        )
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'
        ] = 'attachment; filename=shopping_cart.csv'
        writer = csv.writer(response)
        writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])
        for ingredient in ingredients:
            _ = writer.writerow(
                [
                    ingredient['ingredient__name'],
                    ingredient['total'],
                    ingredient['ingredient__measurement_unit'],
                ],
            )
        return response
