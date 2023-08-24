import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.utils import check_favorites, check_is_in_shopping_cart
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.serializers import SpecialUserSerializer


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
        return check_favorites(self.context.get('request').user, object)

    def get_is_in_shopping_cart(self, object):
        return check_is_in_shopping_cart(
            self.context.get('request').user,
            object,
        )

    def add_tags_and_ingredients(self, tags, ingredients, model):
        model.tags.set(tags)
        for ingredient in ingredients:
            IngredientInRecipe.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_and_ingredients(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name,
        )
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        errors = []
        if 'tags' not in validated_data:
            errors.append('Поле tags обязательно для заполнения.')
        if 'ingredients' not in validated_data:
            errors.append('Поле ingredients обязательно для заполнения.')
        if errors:
            raise serializers.ValidationError(errors)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.add_tags_and_ingredients(tags, ingredients, instance)
        return super().update(instance, validated_data)

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
        return check_favorites(self.context.get('request').user, object)

    def get_is_in_shopping_cart(self, object):
        return check_is_in_shopping_cart(
            self.context.get('request').user,
            object,
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
