import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientInRecipeSerializer(many=True, write_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = RepresentationIngredientSerializer(
            instance.ingredient_in_recipe.all(),
            many=True,
        ).data
        response_tags = []
        for tag in representation['tags']:
            response_tags.append(Tag.objects.filter(id=tag).values()[0])
        representation['tags'] = response_tags
        return representation


class RecipeReadOnlySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = RepresentationIngredientSerializer(
        many=True,
        source='ingredient_in_recipe',
        read_only=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
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
