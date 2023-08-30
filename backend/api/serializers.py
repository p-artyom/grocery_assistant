from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.fields import Base64ImageField
from core.utils import add_tags_and_ingredients, checking_availability
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.serializers import SpecialUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RepresentationIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True,
    )
    author = SpecialUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, write_only=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'author',
            'created',
            'modified',
        )

    def get_is_favorited(self, object):
        return checking_availability(
            self.context.get('request').user,
            object,
            Favorite,
        )

    def get_is_in_shopping_cart(self, object):
        return checking_availability(
            self.context.get('request').user,
            object,
            ShoppingCart,
        )

    def validate_ingredients(self, value):
        ingredients = []
        for ingredient in value:
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться в рецепте!',
                )
            ingredients.append(ingredient['id'])
        return value

    def validate(self, data):
        errors = []
        if 'ingredients' not in data:
            errors.append('Поле ingredients обязательно для заполнения.')
        if 'tags' not in data:
            errors.append('Поле tags обязательно для заполнения.')
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        add_tags_and_ingredients(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        add_tags_and_ingredients(tags, ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = RepresentationIngredientSerializer(
            instance.ingredient_in_recipe.all(),
            many=True,
        ).data
        representation['tags'] = TagSerializer(
            instance.tags.all(),
            many=True,
        ).data
        return representation


class RecipeReadOnlySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = SpecialUserSerializer(read_only=True)
    ingredients = RepresentationIngredientSerializer(
        many=True,
        source='ingredient_in_recipe',
        read_only=True,
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'author',
            'created',
            'modified',
        )

    def get_is_favorited(self, object):
        return checking_availability(
            self.context.get('request').user,
            object,
            Favorite,
        )

    def get_is_in_shopping_cart(self, object):
        return checking_availability(
            self.context.get('request').user,
            object,
            ShoppingCart,
        )


class RecipeInActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
